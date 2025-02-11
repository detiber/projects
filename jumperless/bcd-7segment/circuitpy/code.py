import board
# from digitalio import DigitalInOut, Direction, Pull
# import time
from jumperless import Jumperless
from bcd import BCDEncoder
from sevenSeg import SevenSeg

bcdEncoder = BCDEncoder(13)
sevenSeg = SevenSeg(50)

# Note: this needs to match the defninitions in the arduino sketch
nanoPins = {
    "A0": "D2",
    "A1": "D3",
    "A2": "D4",
    "A3": "D5",
    "LT": "D7",
    "BI": "D8",
}

connections = []

# Map ground and power pins for the bcd encoder
for pin in bcdEncoder.groundPins:
    connections.append(("GND", bcdEncoder.rowForPin(pin)))

for pin in bcdEncoder.power5vPins:
    connections.append(("5V", bcdEncoder.rowForPin(pin)))

for pin in bcdEncoder.power3v3Pins:
    connections.append(("3V3", bcdEncoder.rowForPin(pin)))

# Map the common anode pins for the 7 segment display
for pin in sevenSeg.power3v3Pins:
    connections.append(("3V3", sevenSeg.rowForPin(pin)))

# Map the bcd outputs to the 7 segment display inputs    
for k,source in bcdEncoder.outputPins.items():
    dest=sevenSeg.inputPins[k]
    connections.append((bcdEncoder.rowForPin(source), sevenSeg.rowForPin(dest)))

# Map the Nano pins to the bcd encoder inputs
for k,source in nanoPins.items():
    dest=bcdEncoder.inputPins[k]
    connections.append((source, bcdEncoder.rowForPin(dest)))

str_list = [f"{str(x)}-{str(y)}" for (x, y) in connections]
command = f"f {",".join(str_list)},\n"

print(command)

# jumperless = Jumperless(board.RX, board.TX)
# jumperless.make_connections(connections)
