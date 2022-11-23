import serial
import serial.tools.list_ports
import threading
import sys


class PySerial:
    def inputThread(self):
        print("Input thread")
        while True:
            command = input()
            if command.lower() == "exit":
                self.kill_session = True
                break

            command = bytes(command, encoding="utf-8")
            print(f"Sending {command} command")
        print("Killing input thread")


    def serialReceiveThread(self):
        print("uart thread")
        # CMD input thread will close the program
        while not self.kill_session:
            data = self.device.readline()
            #print(data)
        print("Killing serial rx thread")

    def __init__(self, port=None, baudrate=115200):
        self.kill_session = False
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

        self.device = serial.Serial(devices[int(port)][0], baudrate)

    def __del__(self):
        # Close the connection once port is unused
        self.device.close()

    def loop(self):
        self.input_thread = threading.Thread(target=self.inputThread, daemon=True)
        self.serial_rx_thread = threading.Thread(target=self.serialReceiveThread, daemon=True)

        self.input_thread.start()
        self.serial_rx_thread.start()

        self.input_thread.join()
        self.serial_rx_thread.join()


s = PySerial()
s.loop()

