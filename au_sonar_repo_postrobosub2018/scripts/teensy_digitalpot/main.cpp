#include <Wire.h>
#include <Arduino.h>

int NC = 0b00101110; // 0b00101111 - 47
int VDD = 0b00101100;
int GND = 0b00101111;
int newValue = 0;
int lastValue = 0;
int address = NC;
bool event = false;
bool addrflag = true;
bool valueflag = false;
int counter = 0 ;

void enableWiperPositionChange();
void checkConnection(int address);
void setResistorValue(int address, int inputValue);
void serialEvent();
int readRDAC(int address);
int receiveI2C(int address);

void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(5000); // Wait a few seconds for shit to load
  checkConnection(NC);
  checkConnection(VDD);
  checkConnection(GND);
}

void loop() {
  if (event) {
    if(newValue < 1024 && newValue >= 0) {
      setResistorValue(address, newValue);
      lastValue = newValue;
    }
    else {
      newValue = lastValue;
    }
    event = false;
  }
}

void checkConnection(int address) {
  Wire.beginTransmission(address); // full address
  Wire.write(28); // 00011100
  Wire.write(2); // 00000010
  Serial.println(Wire.endTransmission());
}

void serialEvent() {
  while (Serial.available()) {
    if (addrflag) {
      int temp = Serial.parseInt();
      switch (temp) {
        case 0:
          break;
        case 1:
          address = NC;
          addrflag = false; valueflag = true;
          Serial.print("Address: "); Serial.println(address);
          break;
        case 2:
          address = VDD;
          addrflag = false; valueflag = true;
          Serial.print("Address: "); Serial.println(address);
          break;
        case 3:
          address = GND;
          addrflag = false; valueflag = true;
          Serial.print("Address: "); Serial.println(address);
          break;
        default:
          Serial.println("Address error");
      }
    }
    else if (valueflag) {
      newValue = Serial.parseInt();
      if (newValue == 0) {}
      else {
        addrflag = true; valueflag = false;
        Serial.print("New Value: "); Serial.println(newValue);
        event = true;
      }
    }
  }
}

void setResistorValue(int address, int inputValue) {

   // Generating sequence for given value
   if(inputValue < 255) {
     Wire.beginTransmission(address);
     Wire.write(4);
     Wire.write(inputValue);
     Wire.endTransmission();
   }
   else if(inputValue < 512) {
     Wire.beginTransmission(address);
     Wire.write(5);
     Wire.write((inputValue-256));
     Wire.endTransmission();
   }
   else if(inputValue < 768) {
     Wire.beginTransmission(address);
     Wire.write(6);
     Wire.write((inputValue-512));
     Wire.endTransmission();
   }
   else if(inputValue <= 1024) {
     Wire.beginTransmission(address);
     Wire.write(7);
     Wire.write((inputValue-768));
     Wire.endTransmission();
   }

   Serial.print("Changed address "); Serial.print(address);
   Serial.print(" to "); Serial.println(inputValue);

   /* TO DO: Add redundancy check using readRDAC*/
}

int readRDAC(int address) {   // command 1 from the Datasheet
  Wire.beginTransmission(address);
  Wire.write(8);
  Wire.write(0);
  Wire.endTransmission();
  int cInt = receiveI2C(address);
  return cInt;
}

int receiveI2C(int address) {
   Wire.beginTransmission(address);
   Wire.requestFrom(address, 2);
   int cInt = 0;
   int counter = 0;
   while(Wire.available())    // slave may send less than requested
    {
     int c = Wire.read();    // receive a byte as character
     counter = counter + 1;
     if(counter == 1) {
       cInt = c*256;
     }
     if(counter != 1) {
       cInt = cInt+c;
     }
    }
   Wire.endTransmission();
   return cInt;
}
