import serial
import serial.tools.list_ports


class PySerial:
    def __init__(self, port=None):
        ports = serial.tools.list_ports.comports()
        devices = []
        i = 0

        if port == None:
            for i, device in enumerate(ports):
                devices.append(device)
                print(f"{i}) {device[0]}: {device[1]} [{device[2]}]")

            if len(devices) > 1:
                port = input(f"Select serial port [0 - {i}]")
            else:
                port = 0

        self.device = serial.Serial(devices[int(port)][0])

    def __del__(self):
        # Close the connection once port is unused
        self.device.close()


s = PySerial()
