# Copyright 2025 Guy Dupont.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
`jumperless`
=================================================

Jumperless

* Author(s): Guy Dupont, Jason DeTiberus

Implementation Notes
--------------------

**Hardware:**

* `Adafruit Device Description
  <hyperlink>`_ (Product ID: <Product Number>)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

from busio import UART
from digitalio import DigitalInOut, Direction

__version__ = "0.0.0+auto.0"
__repo__ = "<repo github link>"

EOT = b'\x04'
ACK = b'\x06'
STX = b'\x02'
RDY = b'\x01'

class Nano:
    """Arduino Nano.
    """

    def __init__(self):
        self.digitalOutputs={}
        self.digitalInputs={}

    def addDigitalOutput(self, name, pin, pinName):
        """Configures a digital output.

        :param str name: The name to use for referencing the pin.
        :param ~microcontroller.Pin pin: The microcontroller pin.
        :param str pinName: The string name for the pin.
        """
        self.digitalOutputs[name]=pinName
        do = DigitalInOut(pin)
        do.direction = Direction.OUTPUT
        return do

    def addDigitalInput(self, name, pin, pinName):
        self.digitalInputs[name]=pinName
        do = DigitalInOut(pin)
        do.direction = Direction.INPUT
        return do

class Jumperless:
    """Jumperless.

    :param ~microcontroller.Pin rx_pin: The pin to use for rx.
    :param ~microcontroller.Pin tx_pin: The pin to use for tx.
    :param int baudrate: The baudrate to use. Defaults to :const:`115200`
    """

    def __init__(self, rx_pin, tx_pin, baudrate=115200):
        self.uart = UART(tx_pin, rx_pin, baudrate=baudrate)
        self.connections = []

    # def probe_pin(self):
    #     print("Clearing the input buffer")
    #     self.uart.reset_input_buffer()
    #     print("Sending \"j\"")
    #     self.uart.write("j")
    #     result = self.uart.readline()
    #     print("result: {}".format(result))
    #     while result == None:
    #         result = self.uart.readline()
    #         print("result: {}".format(result))
    #     return result

    def add_connection(self, source, dest):
        """Adds a connection from source to dest.

        :param int,str source: connection source
        :param int,str dest: connection destination
        """
        connection = (source, dest)
        print("adding connection: {}".format(connection))
        self.connections.append(connection)

    def make_connections(self):
        """Commits the registered connections to Jumperless.
        """
        # the transmission order is:
        # Arduino (A) - Jumperless (J)
        # 
        # each step waits for the next acknowledgement

        # A -> J : STX (\x02)
        # A <- J : RDY (\x01)
        # A -> J : sends one bridge (trailing comma)  6-9,
        # A <- J : ACK (\x06)
        # A -> J : sends another bridge (trailing comma)  4-20,
        # A <- J : ACK (\x06)
        # repeat until all bridges are sent
        # A -> J : EOT (\x04)

        # clear the input buffer
        print("Clearing the input buffer")
        self.uart.reset_input_buffer()

        print("Sending STX")
        self.uart.write(STX)
        resp = self.uart.read(1)
        if resp != RDY:
            print(f"received a response other than RDY: {resp}")
            return

        for (source,dest) in self.connections:
            connection = f"{str(source)}-{str(dest)},"
            print(f"Sending connection: {connection}")
            self.uart.write(connection)
            resp = self.uart.read(1)
            if resp != ACK:
                print(f"received a response other than ACK: {resp}")
                return
            
        print("sending EOT")
        self.uart.write(EOT)
