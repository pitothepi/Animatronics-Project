static const int analogpins[] = {A3, A4, A5, A6, A7};

void setup() {
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly: 
  if (Serial.available() > 0) {
    int command = Serial.read();
    //Serial.println(command);
    int reading = analogRead(analogpins[command-48]);
    Serial.println(reading);
  }
}
