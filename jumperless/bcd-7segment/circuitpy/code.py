import board
import time
from digitalio import DigitalInOut, Direction
from jumperless import Jumperless
from bcd import BCDEncoder
from sevenSeg import SevenSeg

bcdEncoder = BCDEncoder(13)
sevenSeg = SevenSeg(50)

jumperless = Jumperless(board.D0, board.D1)

# Map ground and power pins for the bcd encoder
for pin in bcdEncoder.groundPins:
    jumperless.add_connection("GND", bcdEncoder.rowForPin(pin))

for pin in bcdEncoder.power5vPins:
    jumperless.add_connection("5V", bcdEncoder.rowForPin(pin))

for pin in bcdEncoder.power3v3Pins:
    jumperless.add_connection("3V3", bcdEncoder.rowForPin(pin))

# Map the common anode pins for the 7 segment display
for pin in sevenSeg.power3v3Pins:
    jumperless.add_connection("3V3", sevenSeg.rowForPin(pin))

# Map the bcd outputs to the 7 segment display inputs    
for k,source in bcdEncoder.outputPins.items():
    dest=sevenSeg.inputPins[k]
    jumperless.add_connection(bcdEncoder.rowForPin(source), sevenSeg.rowForPin(dest))

a0 = DigitalInOut(board.D2)
a0.direction = Direction.OUTPUT
jumperless.add_connection("D2", bcdEncoder.rowForPin(bcdEncoder.inputPins["A0"]))

a1 = DigitalInOut(board.D3)
a1.direction = Direction.OUTPUT
jumperless.add_connection("D3", bcdEncoder.rowForPin(bcdEncoder.inputPins["A1"]))

a2 = DigitalInOut(board.D4)
a2.direction = Direction.OUTPUT
jumperless.add_connection("D4", bcdEncoder.rowForPin(bcdEncoder.inputPins["A2"]))

a3 = DigitalInOut(board.D5)
a3.direction = Direction.OUTPUT
jumperless.add_connection("D5", bcdEncoder.rowForPin(bcdEncoder.inputPins["A3"]))

lt = DigitalInOut(board.D7)
lt.direction = Direction.OUTPUT
jumperless.add_connection("D7", bcdEncoder.rowForPin(bcdEncoder.inputPins["LT"]))

bi = DigitalInOut(board.D8)
bi.direction = Direction.OUTPUT
jumperless.add_connection("D8", bcdEncoder.rowForPin(bcdEncoder.inputPins["BI"]))

jumperless.make_connections()

def blank():
    print("Blank")
    bi.value = False

def lampTestEnable():
    print("Lamp Test Enable")
    bi.value = True
    lt.value = False

def lampTestDisable():
    print("Lamp Test Disable")
    lt.value = True

def displayNum(num):
    bi.value = True
    lt.value = True
    a0.value = num & 1
    a1.value = (num >> 1) & 1
    a2.value = (num >> 2) & 1
    a3.value = (num >> 3) & 1

blank()

lampTestEnable()
time.sleep(1)

lampTestDisable()
blank()
time.sleep(1)

while True:
    for i in range(10):
        displayNum(i)
        time.sleep(1)
