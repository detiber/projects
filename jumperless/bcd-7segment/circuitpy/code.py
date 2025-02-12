import board
import time
from jumperless import Jumperless, Nano
from bcd import BCDEncoder
from sevenSeg import SevenSeg

bcdEncoder = BCDEncoder(13)
sevenSeg = SevenSeg(50)

jumperless = Jumperless(board.D0, board.D1)
nano = Nano()

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

a0 = nano.addDigitalOutput("A0", board.D2, "D2")
a1 = nano.addDigitalOutput("A1", board.D3, "D3")
a2 = nano.addDigitalOutput("A2", board.D4, "D4")
a3 = nano.addDigitalOutput("A3", board.D5, "D5")
lt = nano.addDigitalOutput("LT", board.D7, "D7")
bi = nano.addDigitalOutput("BI", board.D8, "D8")

for k,source in nano.digitalOutputs.items():
    dest=bcdEncoder.inputPins[k]
    jumperless.add_connection(source, bcdEncoder.rowForPin(dest))

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
