#include <Arduino.h>

int main(void)
{
  init();

  /*** 写setup***/
  Serial.begin(9600);
  pinMode(12,OUTPUT);

  /*** 写loop***/
  while(1) {
    digitalWrite(12,HIGH);
    delay(1000);
    digitalWrite(12,LOW);
    delay(1000);

    /***跳出循环的方法***/    
    if(Serial.read()=='b')  break;
  }

  /***********************/
  return 0;
}