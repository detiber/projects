# Jumperless experiment using a bcd to seven segment display encoder

## Requirements

- Jumperless breadboard
- KYX-3101B 7 segment display
- DM74LS47 BCD encoder

## Setup

1. Place components on the jumperless breadboard
2. Update generateNodeList.py for the pin 1 locations
3. Run generateNodeList.py to get the nodelist for use with the Jumperless cli
4. Run the jumperless cli, selecting the slot you desire, then paste the nodelist created above
5. Flash bcd-7segment.ino onto the Arduino Nano connected to the jumperless
