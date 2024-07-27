#include <Arduino.h>
#include "DHT11.h"

DHT11 myDHT11(2);

void setup()      //Arduino程序初始化程序放在这里，只在开机时候运行一次
{             
  Serial.begin(9600); //设置通讯的波特率为9600
  Serial.println("Welcome to use!");  //发送的内容
  Serial.println("I love DIUSTOU");  //发送的内容
}

void loop()     //Arduino程序的主程序部分，循环运行内部程序
{
  myDHT11.DHT11_Read();               //读取温湿度值
  Serial.print("HUMI = ");
  Serial.print(myDHT11.HUMI_Buffer_Int);
  Serial.println(" %RH");

  Serial.print("TMEP = ");
  Serial.print(myDHT11.TEM_Buffer_Int);
  Serial.println(" C");
  delay(1000);        //延时1s
}
