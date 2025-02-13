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
