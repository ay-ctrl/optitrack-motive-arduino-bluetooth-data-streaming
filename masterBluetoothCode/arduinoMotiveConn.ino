#include <SoftwareSerial.h>

const byte rxpin = 3;
const byte txpin = 2;
SoftwareSerial BTSerial(rxpin,txpin); // rx/tx

void setup(){
  pinMode(rxpin, INPUT);
  pinMode(txpin, OUTPUT);
  Serial.begin(9600);
  BTSerial.begin(38400);
}

String line="";

void loop(){

  if(BTSerial.available())
  {
    Serial.write(BTSerial.read());
  }

  if(Serial.available())
  {
    String data=Serial.readStringUntil('\n');
    BTSerial.println(data);
  }
  
  // for at mode
  /* 
  if(Serial.available())
  {
    BTSerial.write(Serial.read());
  }
  */
}

