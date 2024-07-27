#include <MsTimer2.h>

unsigned int motor1=0;	 //计左电机码盘脉冲值
unsigned int motor2=0;	 //计右电机码盘脉冲值
unsigned int speed1=0;	 //计左电机速度值
unsigned int speed2=0;	 //计右电机速度值
unsigned int k=0;

void flash(){
  speed1=motor1;
  speed2=motor2;
  motor1=0;	 	//重新定义motor1的值
  motor2=0;		//重新定义motor1的值
}

void setup() {
  Serial.begin(9600);
   attachInterrupt(0, left_motor, RISING);  
  attachInterrupt(1,right_motor,RISING);
  MsTimer2::set(1000, flash);	// 中断设置函数，每 500ms 进入一次中断
  MsTimer2::start();		//开始计时
}

void loop() {
    Serial.print("left motor:");
    Serial.print(motor1);
    Serial.print("\tright motor:");
    Serial.println(motor2);
}

void left_motor()	//触发函数
{
  motor1++;	
}

void right_motor()	//触发函数
{
  motor2++;	
}
