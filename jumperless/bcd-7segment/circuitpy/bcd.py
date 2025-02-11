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
