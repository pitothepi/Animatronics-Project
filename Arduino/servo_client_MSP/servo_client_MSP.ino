#include <Servo.h>

Servo servos[5];

static const int POWER_PIN = P1_0;
static const int PINS[] = {P2_3, P2_4, P2_5, P1_6, P1_7};

int minBend[] = {30, 40, 38, 50, 30};
int maxBend[] = {55, 64, 68, 30, 70};

int power(int x, int y) {
  int total = 1;
  for (int i = 0; i < y; i++) {
    total *= x;
  }
  return total;
}

int bendToAngle(int bend, int pin) {
  return 180 - int(float(bend - minBend[pin]) / (maxBend[pin] - minBend[pin]) * 180 + .5);
}

int getData() {
  digitalWrite(POWER_PIN, LOW);
  delay(5);
  unsigned long start = millis();
  int vals[6];
  int val = Serial.read();
  int count = 0;
  while (int(val) != 59) {
    if (millis() > start + 1000 || count > 5) {
      return -1;
    }
    vals[count] = val - int('0');
    count++;
    val = Serial.read();
  }
  int intVal = 0;
  for (int i = 0; i < count; i++) {
    intVal += vals[i] * power(10, (count - i));
  }
  digitalWrite(POWER_PIN, HIGH);
  return intVal / 10;
}

void setup() {
  Serial.begin(9600);
  pinMode(POWER_PIN , OUTPUT);
  digitalWrite(POWER_PIN, HIGH);
  int i;
  for (i = 0; i < (sizeof(servos) / sizeof(Servo)); i++) {
    servos[i].attach(PINS[i]);
    servos[i].write(90);
  }
}

void loop() {
  if (Serial.available() > 0) {
    int data = getData();
    int pin = data % 10;
    int pos = data / 10;
    servos[pin].write(bendToAngle(pos, pin));
  }
  delay(5);
}
