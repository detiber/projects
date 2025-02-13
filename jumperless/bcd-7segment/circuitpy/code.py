import board
import time
import usb_cdc
import sys
import asyncio
from digitalio import DigitalInOut
from jl import Jumperless, Nano
from bcd import BCDEncoder
from sevenSeg import SevenSeg

class Continue:
    def __init__(self, enabled=True):
        self.value = enabled

async def blink_led(pin, enabled):
    with DigitalInOut(pin) as led:
        led.switch_to_output()
        while enabled.value:
            led.value = not led.value
            await asyncio.sleep(0.1)

async def prompt(message, enabled):
    usb_cdc.console.reset_input_buffer()
    print(message)
    while usb_cdc.console.in_waiting == 0:
        await asyncio.sleep(0)

    enabled.value = False
    response = sys.stdin.readline()
    print("response: {}".format(response))
    return response

async def prompt_and_blink(message, pin):
    enabled = Continue()
    blink_task = asyncio.create_task(blink_led(pin, enabled))
    prompt_task = asyncio.create_task(prompt(message, enabled))
    result = await asyncio.gather(blink_task, prompt_task)
    return result[1]

print("Hello")
asyncio.run(prompt_and_blink("Press enter to continue", board.LED_B))
bcdPin1 = asyncio.run(prompt_and_blink("Type pin1 location for the bcd encoder and hit enter", board.LED_B))
bcd1 = int(bcdPin1.strip())
sevenSegPin1 = asyncio.run(prompt_and_blink("Type pin1 location for the seven segment display and hit enter", board.LED_B))
ss1 = int(sevenSegPin1.strip())

jumperless = Jumperless(board.D0, board.D1)
nano = Nano()

bcdEncoder = BCDEncoder(bcd1)
sevenSeg = SevenSeg(ss1)

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
