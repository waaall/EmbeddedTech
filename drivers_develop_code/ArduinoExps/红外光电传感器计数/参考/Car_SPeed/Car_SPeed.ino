unsigned int motor1=0;	 //计左电机码盘脉冲值
unsigned int motor2=0;	 //计右电机码盘脉冲值

void setup() {
  Serial.begin(9600);
  attachInterrupt(0, left_motor, RISING);  
  attachInterrupt(1, right_motor, RISING);
}

void loop() {
    Serial.print("left motor:");
    Serial.print(motor1);
    Serial.print("\tright motor:");
    Serial.println(motor2);
    
}

void left_motor()            //触发函数
{
  motor1++;	
  if(motor1>=99)
    motor1=0;
}

void right_motor()            //触发函数
{
  motor2++;	
  if(motor2>=99) motor2=0;
}
