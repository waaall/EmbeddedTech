const int MOTOR_P = 2;                                      // 电机正极
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(MOTOR_P, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(2000);
  Motor_Forward();
  delay(2000);
  Motor_Stop();
}

void Motor_Forward(){
  Serial.println("forward...");
  digitalWrite(MOTOR_P, HIGH);
}

void Motor_Stop(){
  Serial.println("stop...");
  digitalWrite(MOTOR_P, LOW);
}