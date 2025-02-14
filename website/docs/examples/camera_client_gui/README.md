---
id: camera-client-gui
title: Camera Client GUI
---

### [Link to `camera_client_gui/main.py`](https://github.com/farm-ng/amiga-dev-kit/blob/main/brain/examples/camera_client_gui/main.py)

![Peek 2022-09-02 12-46](https://user-images.githubusercontent.com/5157099/188124779-41f4d519-78d4-453e-9b90-b3d730762b81.gif)

This example implements the [OakCameraClient](/docs/reference/brain/farm_ng/oak/client#oakcameraclient-objects) in a GUI application using [Kivy](https://kivy.org/).

The requirements to run this example are to have a [farm-ng brain](/docs/brain/) running Oak cameras and that your PC is on the same local network as the brain.

### 1. Install the [farm-ng Brain ADK package](/docs/brain/brain-install)

### 2. Install the example's dependencies

:::tip

It is recommended to also install these dependencies and run the example in the brain ADK virtual environment.

:::

```bash
# assuming you're already in the amiga-dev-kit/ directory
cd brain/examples/camera_client_gui
```
```bash
pip3 install -r requirements.txt
```

### 3. Execute the Python script

```bash
python3 main.py --port 50051
```

:::info
By default, the camera address is assumed top be `localhost`.
:::

### 4. Customize the run

Let's have some fun and stream the camera to your laptop over the Wifi.

:::tip
You need to discover the WiFi address of your Amiga Brain using the `WifiClient` (coming soon)
:::

```bash
python3 main.py --help

# usage: amiga-camera-app [-h] --port PORT [--address ADDRESS] [--stream-every-n STREAM_EVERY_N]

# optional arguments:
#   -h, --help            show this help message and exit
#   --port PORT           The camera port.
#   --address ADDRESS     The camera address
#   --stream-every-n STREAM_EVERY_N
#                         Streaming frequency
```
Usage example:

```bash
python3 main.py --address 192.168.1.93 --port 50051
```
