#!/bin/python
from TcpClient import ResponseType, TCPClient
from gpiozero import LED
from pyclbr import Function
import sys
import time


class App():
    def __init__(self) -> None:
        if len(sys.argv) == 2:
            self.station = sys.argv[1]
        else:
            self.station = "Office"

        self.tcp_client = TCPClient("10.0.0.76", 13000, self.station)
        self.card_string = ""
        self.occupied = False
        self.pin = LED(4)  # Corresponds to GPIO4 aka pin 7

        print(f"BUCAM Station ({self.station}) started.")

        while True:
            card_string = input()
            response = self.tcp_client.send_access(self.card_string)
            if response.type == ResponseType.OK:
                self.open_door(5)
            else:
                print('invalid card.')

    def open_door(self, timeout) -> None:
        self.pin.on()
        time.sleep(timeout)
        self.pin.off()

if __name__ == "__main__":
    app = App()

