#include <Servo.h>

Servo servos[5];

static const int POWER_PIN = P1_0;
static const int PINS[] = {P2_3, P2_4, P2_5, P1_6, P1_7};

int minBend = 30;
int maxBend = 70;

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
  //Serial.println("Getting");
  digitalWrite(POWER_PIN, LOW);
  delay(5);
  unsigned long start = millis();
  int vals[6];
  int val = Serial.read();
  int count = 0;
  while (int(val) != 59) {
    //Serial.print(val);
    if (millis() > start + 1000 || count > 5) {
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
    //Serial.println(intVal);
    //Serial.println(vals[i]);
    intVal += vals[i] * power(10, (count - i));
  }
  //Serial.flush();
  //digitalWrite(P1_0, HIGH);
  //Serial.println("Done Getting");
  //Serial.println(intVal / 10);
  digitalWrite(POWER_PIN, HIGH);
  return intVal / 10;
}

void setup() {
  Serial.begin(9600);
  //Serial.println(int('0'));
  pinMode(POWER_PIN ,OUTPUT);
  digitalWrite(POWER_PIN, HIGH);
  int i;
  for (i = 0; i < (sizeof(servos) / sizeof(Servo)); i++) {
    servos[i].attach(PINS[i]);
    servos[i].write(90);
  }
}

void loop() {
  // put your main code here, to run repeatedly: 
  if (Serial.available() > 0) {
    int data = getData();
    int pin = data % 10;
    int pos = data / 10;
    servos[pin].write(bendToAngle(pos));
  }
  delay(5);
}
