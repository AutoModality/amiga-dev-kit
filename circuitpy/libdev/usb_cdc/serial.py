class Serial:
    """Receives cdc commands over USB"""
    def __init__(self) -> None:
        """You cannot create an instance of `usb_cdc.Serial`.
        The available instances are in the ``usb_cdc.serials`` tuple."""
        ...
    def read(self, size: int = 1) -> bytes:
        """Read at most ``size`` bytes. If ``size`` exceeds the internal buffer size
        only the bytes in the buffer will be read. If `timeout` is > 0 or ``None``,
        and fewer than ``size`` bytes are available, keep waiting until the timeout
        expires or ``size`` bytes are available.
        :return: Data read
        :rtype: bytes"""
        ...
    def readinto(self, buf: WriteableBuffer) -> int:
        """Read bytes into the ``buf``. Read at most ``len(buf)`` bytes. If `timeout`
        is > 0 or ``None``, keep waiting until the timeout expires or ``len(buf)``
        bytes are available.
        :return: number of bytes read and stored into ``buf``
        :rtype: int"""
        ...
    def readline(self, size: int = -1) -> Optional[bytes]:
        r"""Read a line ending in a newline character ("\\n"), including the newline.
        Return everything readable if no newline is found and ``timeout`` is 0.
        Return ``None`` in case of error.
        This is a binary stream: the newline character "\\n" cannot be changed.
        If the host computer transmits "\\r" it will also be included as part of the line.
        :param int size: maximum number of characters to read. ``-1`` means as many as possible.
        :return: the line read
        :rtype: bytes or None"""
        ...
    def readlines(self) -> List[Optional[bytes]]:
        """Read multiple lines as a list, using `readline()`.
        .. warning:: If ``timeout`` is ``None``,
          `readlines()` will never return, because there is no way to indicate end of stream.
        :return: a list of the line read
        :rtype: list"""
        ...
    def write(self, buf: ReadableBuffer) -> int:
        """Write as many bytes as possible from the buffer of bytes.
        :return: the number of bytes written
        :rtype: int"""
        ...
    def flush(self) -> None:
        """Force out any unwritten bytes, waiting until they are written."""
        ...