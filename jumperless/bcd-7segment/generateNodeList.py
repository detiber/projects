class BCDEncoder:
    # pin1Location is the breadboard row that pin 1 is connected to on the jumperless
    def __init__(self, pin1Location):
        if pin1Location <= 30:
            # pin1 is up, so decrement for pins 1-8
            self.pinToBreadBoard = list(range(pin1Location, pin1Location-8, -1))
            # Add 30 to the location of pin 8 to get pin 9's location
            # then increment from pins 9-16
            pin9Location=self.pinToBreadBoard[-1]+30
            self.pinToBreadBoard.extend(list(range(pin9Location, pin9Location+8)))
        else:
            # pin1 is down, so increment for pins 1-8
            self.pinToBreadBoard = list(range(pin1Location, pin1Location+8))
            # Subtract 30 from the location of pin 8 to get pin 9's location
            # then decrement from pins 9-16
            pin9Location=self.pinToBreadBoard[-1]-30
            self.pinToBreadBoard.extend(list(range(pin9Location, pin9Location-8, -1)))

        self.groundPins=[8]
        self.power5vPins=[16]
        # We are ignoring RBI, but pinning it High, so include it here
        self.power3v3Pins=[5]
        self.inputPins={
            "A1": 1,
            "A2": 2,
            "LT": 3,
            "BI": 4,
            "A3": 6,
            "A0": 7,
        }
        self.outputPins={
            "F": 15,
            "G": 14,
            "A": 13,
            "B": 12,
            "C": 11,
            "D": 10,
            "E": 9,
        }

    def rowForPin(self, pin):
        return self.pinToBreadBoard[pin-1]
    
    def pinForRow(self, row):
        return self.pinToBreadBoard.index(row)+1

class SevenSeg:
    # pin1Location is the breadboard row that pin 1 is connected to on the jumperless
    def __init__(self, pin1Location):
        if pin1Location <= 30:
            # pin1 is up, so decrement for pins 1-7
            self.pinToBreadBoard = list(range(pin1Location, pin1Location-7, -1))
            # Add 30 to the location of pin 7 to get pin 8's location
            # then increment from pins 8-14
            pin8Location=self.pinToBreadBoard[-1]+30
            self.pinToBreadBoard.extend(list(range(pin8Location, pin8Location+7)))
        else:
            # pin1 is down, so increment for pins 1-7
            self.pinToBreadBoard = list(range(pin1Location, pin1Location+7))
            # Subtract 30 from the location of pin 8 to get pin 9's location
            # then decrement from pins 8-14
            pin8Location=self.pinToBreadBoard[-1]-30
            self.pinToBreadBoard.extend(list(range(pin8Location, pin8Location-7, -1)))

        self.power3v3Pins=[3,14]
        self.inputPins={
            "A": 1,
            "B": 13,
            "C": 10,
            "D": 8,
            "E": 7,
            "F": 2,
            "G": 11,
        }

    def rowForPin(self, pin):
        return self.pinToBreadBoard[pin-1]
    
    def pinForRow(self, row):
        return self.pinToBreadBoard.index(row)+1

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

print("f {")

# Map ground and power pins for the bcd encoder
for pin in bcdEncoder.groundPins:
    print("GND-{},".format(bcdEncoder.rowForPin(pin)))

for pin in bcdEncoder.power5vPins:
    print("5V-{},".format(bcdEncoder.rowForPin(pin)))

for pin in bcdEncoder.power3v3Pins:
    print("3V3-{},".format(bcdEncoder.rowForPin(pin)))

# Map the common anode pins for the 7 segment display
for pin in sevenSeg.power3v3Pins:
    print("3V3-{},".format(sevenSeg.rowForPin(pin)))

# Map the bcd outputs to the 7 segment display inputs    
for k,source in bcdEncoder.outputPins.items():
    dest=sevenSeg.inputPins[k]
    print("{}-{},".format(bcdEncoder.rowForPin(source), sevenSeg.rowForPin(dest)))

# Map the Nano pins to the bcd encoder inputs
for k,source in nanoPins.items():
    dest=bcdEncoder.inputPins[k]
    print("{}-{},".format(source, bcdEncoder.rowForPin(dest)))

print("}")
