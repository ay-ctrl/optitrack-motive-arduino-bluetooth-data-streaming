#include <SoftwareSerial.h>
SoftwareSerial BTSerial(3, 2);  // RX, TX

void setup() {
  Serial.begin(9600);
  BTSerial.begin(38400);  // HC-05 genelde 9600 baud
  Serial.println("Hazır");
}

void loop() {
  if (BTSerial.available()) {
    String gelen = BTSerial.readStringUntil('\n');
    Serial.print("Slave aldı: ");
    Serial.println(gelen);
  }
}
