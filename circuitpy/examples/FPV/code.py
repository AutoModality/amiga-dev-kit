import board
import busio
import canio
from farm_ng.utils.cobid import CanOpenObject
from farm_ng.utils.general import Axis
from farm_ng.utils.general import TickRepeater
from farm_ng.utils.main_loop import MainLoop
from farm_ng.utils.packet import AmigaControlState
from farm_ng.utils.packet import AmigaRpdo1
from farm_ng.utils.packet import AmigaTpdo1
from farm_ng.utils.packet import Packet
from farm_ng.utils.packet import DASHBOARD_NODE_ID
from farm_ng.utils.packet import AMROS_ID
from struct import pack
from struct import unpack


def parse_packet(packet):
    # https://github.com/robotmaker/Real-time-graphical-representation-of-16-channel-S-BUS-protocol/blob/master/ProcessingSketch_SBUS_16_Channel_Simulation/ProcessingSketch_SBUS_16_Channel_Simulation.pde

    # channel_0 = (packet[1] | packet[2] << 8) & 0x07FF
    # channel_1 = (packet[2] >> 3 | packet[3] << 5) & 0x07FF
    # channel_2 = (packet[3] >> 6 | packet[4] << 2 | packet[5] << 10) & 0x07FF
    # channel_3 = (packet[5] >> 1 | packet[6] << 7) & 0x07FF
    channels = [None] * 16

#    channel_sum = int.from_bytes(packet[1:23], byteorder"little")
    channel_sum = int.from_bytes(packet[1:23], "little")

    for ch in range(0, 16):
        channels[ch] = channel_sum & 0x7ff
        channel_sum = channel_sum >> 11

    if True:
        print('FVP - 0:{:>4} 1:{:>4} 2:{:>4} 3:{:>4} 4:{:>4} 5:{:>4} 6:{:>4} 7:{:>4} 8:{:>4} 9:{:>4} 10:{:>4} 11:{:>4} 12:{:>4} 13:{:>4} 14:{:>4} 15:{:>4} '.
           format(channels[0], channels[1], channels[2], channels[3], channels[4], channels[5], channels[6], channels[7],
           channels[8], channels[9], channels[10], channels[11], channels[12], channels[13], channels[14], channels[15]))
    return channels


class RC0(Packet):

    def __init__(
        self,
        channels,
    ):
        self.format = "<8B"
        self.channels = [None] * 8;
        for ch in range(0, 8):
            self.channels[ch] = int((channels[ch] - 172) / 1639.0 * 255) & 0xff # 0 1811 172 992 1639
        self.stamp()

    def encode(self):
        """Returns the data contained by the class encoded as CAN message data."""
        return pack(self.format, self.channels[0], self.channels[1], self.channels[2], self.channels[3],
        self.channels[4], self.channels[5], self.channels[6], self.channels[7])

    def decode(self, data):
        """Decodes CAN message data and populates the values of the class."""

    def __str__(self):
        return "AMIGA RC0 0:{:>4} 1:{:>4} 2:{:>4} 3:{:>4} 4:{:>4} 5:{:>4} 6:{:>4} 7:{:>4}".format(
            self.channels[0], self.channels[1], self.channels[2], self.channels[3],
            self.channels[4], self.channels[5], self.channels[6], self.channels[7]
        )

class RC1(Packet):

    def __init__(
        self,
        channels,
    ):
        self.format = "<8B"
        self.channels = [None] * 8;
        for ch in range(0, 8):
            self.channels[ch] = int((channels[ch+8] - 172) / 1639.0 * 255) & 0xff # 0 1811 172 992 1639
        self.stamp()

    def encode(self):
        """Returns the data contained by the class encoded as CAN message data."""
        return pack(self.format, self.channels[0], self.channels[1], self.channels[2], self.channels[3],
        self.channels[4], self.channels[5], self.channels[6], self.channels[7])

    def decode(self, data):
        """Decodes CAN message data and populates the values of the class."""

    def __str__(self):
        return "AMIGA RC1 0:{:>4} 1:{:>4} 2:{:>4} 3:{:>4} 4:{:>4} 5:{:>4} 6:{:>4} 7:{:>4}".format(
            self.channels[0], self.channels[1], self.channels[2], self.channels[3],
            self.channels[4], self.channels[5], self.channels[6], self.channels[7]
        )

class FpvApp:
    RC0 = 0x000
    RC1 = 0x100

    def __init__(self, main_loop: MainLoop, can, node_id):
        print('FpvApp')
        self.can = can
        self.main_loop = main_loop
        self.node_id = node_id
        self.uart = busio.UART(
            None, board.RX, baudrate=100000, bits=8, parity=0, stop=2, timeout=0.002, receiver_buffer_size=256
        )

        self.amiga_tpdo1 = None
        self.debug_repeater = TickRepeater(ticks_period_ms=100)
        # send commands to amiga at 20hz
        self.cmd_repeater = TickRepeater(ticks_period_ms=20)

        # TODO calibrate these values
        self.axis2 = Axis(min=172, dz_neg=900, dz_pos=1100, max=1811)

        self.axis3 = Axis(min=172, dz_neg=800, dz_pos=1200, max=1811)

        self.max_speed = 2.5  # meters per second
        self.max_angular_rate = 3.14  # radians per second

    def _register_message_handlers(self):
        self.main_loop.command_handlers[CanOpenObject.TPDO1 | DASHBOARD_NODE_ID] = self._handle_amiga_tpdo1

    def _handle_amiga_tpdo1(self, message):
        self.amiga_tpdo1 = AmigaTpdo1.from_can_data(message.data)

    def send_command(self, channels):
        # don't send commands too frequently to Amiga
        if not self.cmd_repeater.check():
            return

        if channels[14] < 500:
            rpdo1 = AmigaRpdo1(state_req=AmigaControlState.STATE_AUTO_READY, cmd_speed=0, cmd_ang_rate=0)
            self.can.send(canio.Message(id=CanOpenObject.RPDO1 | DASHBOARD_NODE_ID, data=rpdo1.encode()))
        elif channels[14] >= 500 and channels[14] <= 1500:
            cmd_speed = self.max_speed * self.axis2.map(channels[2])
            cmd_ang_rate = self.max_angular_rate * -self.axis3.map(channels[1])
            rpdo1 = AmigaRpdo1(state_req=AmigaControlState.STATE_AUTO_ACTIVE, cmd_speed=cmd_speed, cmd_ang_rate=cmd_ang_rate)
            self.can.send(canio.Message(id=CanOpenObject.RPDO1 | DASHBOARD_NODE_ID, data=rpdo1.encode()))

        rc0 = RC0(channels=channels)
        self.can.send(canio.Message(id=self.RC0 | AMROS_ID, data=rc0.encode()))

        rc1 = RC1(channels=channels)
        self.can.send(canio.Message(id=self.RC1 | AMROS_ID, data=rc1.encode()))

    def iter(self):
        if self.uart.in_waiting >= 25:
            packet = bytearray(self.uart.read(25))
            if packet[0] == 0x0F and packet[24] == 0x00:
                channels = parse_packet(packet)
                self.send_command(channels)
            else:
                print('FVP invalid packet: {}'.format(packet))
                self.uart.reset_input_buffer()


def main():
    MainLoop(AppClass=FpvApp, has_display=False).loop()


main()
