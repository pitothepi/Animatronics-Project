#include <Servo.h>

Servo servo1;

static const int analogpins[] = {A3, A4, A5, A6, A7};
int minBend = 300;
int maxBend = 700;

int power(int x, int y) {
  int total = 1;
  for (int i = 0; i < y; i++) {
    total *= x;
  }
  return total;
}

int bendToAngle(int bend) {
  return 180 - int(float(bend - minBend) / (maxBend - minBend) * 180 + .5);
}

void sendSerialError() {
  Serial.println("error");
  delay(500);
  Serial.flush();
}

int getData() {
  delay(5);
  unsigned long start = millis();
  int vals[5];
  int val = Serial.read();
  int count = 0;
  while (int(val) != 59) {
    //Serial.print(val);
    if (millis() > start + 1000 || count > 4) {
      return -1;
    }
    //Serial.println(val);
    vals[count] = val - int('0');
    count++;
    val = Serial.read();
  }
  //Serial.println("count" + String(count));
  int intVal = 0;
  for (int i = 0; i < count; i++) {
    //Serial.println(vals[i]);
    intVal += vals[i] * power(10, (count - i));
  }
  //Serial.flush();
  //digitalWrite(P1_0,HIGH);
  return intVal / 10;
}

void setup() {
  Serial.begin(9600);
  //Serial.println(int('0'));
  pinMode(P1_0,OUTPUT);
  servo1.attach(P2_3);
  servo1.write(90);
}

void loop() {
  // put your main code here, to run repeatedly: 
  if (Serial.available() > 0) {
    /*int message[] = {-1, -1, -1, -1};
    int lastRead = Serial.read();
    int readCount = 1;
    unsigned long start = millis();
    while (lastRead != 59) {
      message[readCount - 1] = lastRead;
      while (Serial.available() == 0) {
        if (millis() > start + 1000) {
          sendSerialError();
          return;
        }
      }
      lastRead = Serial.read();
      if (lastRead == 59) {
        break;
      }
      readCount++;
      if (readCount > 5) {
        sendSerialError();
        return;
      }
    }
    //Serial.println(command);
    
    Serial.println("");*/
    int data = getData();
    //Serial.println(data);
    //delay(50);
    //int val = Serial.read();
    //Serial.println(val);
    //Serial.flush();
    //Serial.println(
    servo1.write(bendToAngle(data));
  }
  delay(10);
}
