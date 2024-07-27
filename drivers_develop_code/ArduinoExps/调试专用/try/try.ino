#define       MOTOR_PIN   2           // 电机正极
#define       DROP_PIN    4           // 传感器input
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(DROP_PIN, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
  if(digitalRead(DROP_PIN) == 1){
    digitalWrite(MOTOR_PIN, HIGH);
  }else{
    digitalWrite(MOTOR_PIN, LOW);
  }

}
