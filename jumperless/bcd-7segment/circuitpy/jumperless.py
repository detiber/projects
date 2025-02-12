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

import busio

EOT = b'\x04'
ACK = b'\x06'
STX = b'\x02'
RDY = b'\x01'

class Jumperless:
    def __init__(self, rx_pin, tx_pin, baudrate=115200):
        self.uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate)
        self.connections = []

    def add_connection(self, source, dest):
        connection = (source, dest)
        self.connections.append(connection)

    def make_connections(self):
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
        # str_list = [f"{str(x)}-{str(y)}" for (x, y) in self.connections]
        # command = f"f {",".join(str_list)},\n"
        # print(command.encode('utf-8'))
        # self.uart.write(command.encode('utf-8'))
