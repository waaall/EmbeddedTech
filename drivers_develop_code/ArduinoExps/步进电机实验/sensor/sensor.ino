
#include <Arduino.h>

#define A1 2      //引脚命名
#define B1 3
#define C1 4
#define D1 5


void setup()
{
  pinMode(A1,OUTPUT);   //设置引脚为输出引脚
  pinMode(B1,OUTPUT);
  pinMode(C1,OUTPUT);
  pinMode(D1,OUTPUT);
}

void loop()
{
  Phase_A();      //设置A相位
  delay(5);     //改变延时可改变旋转速度

  Phase_B();      //设置B相位
  delay(5);

  Phase_C();      //设置C相位
  delay(5);

  Phase_D();      //设置D相位
  delay(5);

}

void Phase_A()
{
  digitalWrite(A1,HIGH);    //A1引脚高电平 
  digitalWrite(B1,LOW);
  digitalWrite(C1,LOW);
  digitalWrite(D1,LOW);
}

void Phase_B()
{
  digitalWrite(A1,LOW); 
  digitalWrite(B1,HIGH);    //B1引脚高电平 
  digitalWrite(C1,LOW);
  digitalWrite(D1,LOW);
}

void Phase_C()
{
  digitalWrite(A1,LOW); 
  digitalWrite(B1,LOW);
  digitalWrite(C1,HIGH);    //C1引脚高电平 
  digitalWrite(D1,LOW);
}

void Phase_D()
{
  digitalWrite(A1,LOW); 
  digitalWrite(B1,LOW);
  digitalWrite(C1,LOW);
  digitalWrite(D1,HIGH);    //D1引脚高电平 
}
