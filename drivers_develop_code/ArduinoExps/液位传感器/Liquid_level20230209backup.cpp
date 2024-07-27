#include <Arduino.h>

/********需设置的量********/
const int LIQUID_lEVEL_PIN = 6;                            // 光电传感器引脚
const int LED_PIN = 8;                                     // LED正极引脚
const int BUZZER_PIN = 9;                                  // 蜂鸣器引脚


int main(void){
  init();
  /********全局变量********/
  int Status = 0;                               // 液位，1是有水，0是没水（io1是高电平的前提）
  
  /******** setup ********/
  Serial.begin(9600);
  pinMode(LIQUID_lEVEL_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  /******** loop ********/
  while(1) {
    delay(100);
    /***每一滴计数***/
    Status = digitalRead(LIQUID_lEVEL_PIN);         // 读取液位传感器输入    
    if (Status == 1){                              // 液位传感器输出1
      Blink();
    }

    /***结束程序的方法***/    
    if(Serial.read() == 'e') {
      Serial.println("...ending...");
      delay(2000);
      break;
    }
  }
  return 0;
}

/******** 函数：LED闪烁 ********/
void Blink() {
  while(1) {
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(100);
    
    digitalWrite(LED_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);
    delay(100);

    /***停止报警继续运行的方法***/    
    if(Serial.read() == 'g') {
      Serial.println("...go on...");
      break;
    }
  }
}