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

class Jumperless:
    def __init__(self, rx_pin, tx_pin):
        self.uart = busio.UART(tx_pin, rx_pin, baudrate=115200)

    def make_connections(self, connection_list):
        str_list = [f"{str(x)}-{str(y)}" for (x, y) in connection_list]
        command = f"f {",".join(str_list)},\n"
        self.uart.write(command.encode('utf-8'))
