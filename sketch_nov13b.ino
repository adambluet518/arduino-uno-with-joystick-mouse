
const int JOY_X = A0;
const int JOY_Y = A1;
const int JOY_BUTTON = 2;

void setup() {
  Serial.begin(115200);
  pinMode(JOY_BUTTON, INPUT_PULLUP);
}

void loop() {
  int x = analogRead(JOY_X);
  int y = analogRead(JOY_Y);
  int button = digitalRead(JOY_BUTTON);

  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.println(button);

  delay(10);
}
