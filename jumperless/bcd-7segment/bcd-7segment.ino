#include "jumperless.h"

int BCD_A0 = 2;
int BCD_A1 = 3;
int BCD_A2 = 4;
int BCD_A3 = 5;
int BCD_LT = 7;
int BCD_BI = 8;

void setup() {
 
    Serial.begin(9600);
    while (!Serial) {
      ;  // wait for serial port to connect. Needed for native USB port only
    }
    Serial.println("Hello...");

    Jumperless jumperless(115200);
    delay(1500);
    jumperless.AddConnection({"1","20"});
    jumperless.AddConnection({"33","24"});
    jumperless.MakeConnections();
    
    Serial.println("Continuing...");

    pinMode(BCD_A0, OUTPUT);
    pinMode(BCD_A1, OUTPUT);
    pinMode(BCD_A2, OUTPUT);
    pinMode(BCD_A3, OUTPUT);
    pinMode(BCD_LT, OUTPUT);
    pinMode(BCD_BI, OUTPUT);

    blank();

    lampTestEnable();
    delay(1000);

    lampTestDisable();
    blank();
    delay(1000);
}

void blank() {
    Serial.println("Blank");
    digitalWrite(BCD_BI, LOW);
}

void lampTestEnable() {
    Serial.println("Lamp Test Enable");
    digitalWrite(BCD_LT, LOW);
    digitalWrite(BCD_BI, HIGH);
}

void lampTestDisable() {
    Serial.println("Lamp Test Disable");
    digitalWrite(BCD_LT, HIGH);
}

void displayNum(int num) {
  digitalWrite(BCD_BI, HIGH);
  digitalWrite(BCD_LT, HIGH);
  digitalWrite(BCD_A0, num & 1);
  digitalWrite(BCD_A1, (num >> 1) & 1);
  digitalWrite(BCD_A2, (num >> 2) & 1);
  digitalWrite(BCD_A3, (num >> 3) & 1);
}

void zero() {
  digitalWrite(BCD_BI, HIGH);
  digitalWrite(BCD_LT, HIGH);
  digitalWrite(BCD_A3, LOW);
  digitalWrite(BCD_A2, LOW);
  digitalWrite(BCD_A1, LOW);
  digitalWrite(BCD_A0, LOW);
}

void one() {
  digitalWrite(BCD_BI, HIGH);
  digitalWrite(BCD_LT, HIGH);
  digitalWrite(BCD_A3, LOW);
  digitalWrite(BCD_A2, LOW);
  digitalWrite(BCD_A1, LOW);
  digitalWrite(BCD_A0, HIGH);
}

void loop() {
    Serial.println("Count");
    for (int i=0; i < 10; ++i) {
      displayNum(i);
      delay(1000);
    }
}
