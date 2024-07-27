#include <Arduino.h>
#include <LiquidCrystal.h>

/********需设置的量********/
const int COUNT_SENSOR_PIN = 13;              // 光电传感器引脚
const int LED_PIN = 12;                       // LED正极引脚
const int BUZZER_PIN = 9;                 // 红(终止)开关引脚
const int SWITCH_GREEN_PIN = 8;               // 绿(继续)开关引脚
const int HOW_MANY_DROPS = 20;                // 1mL20滴液体
const int PERIOD = 5000;                      // 测速间隔ms，不得小于1000ms
const int WARNING_PERIOD = 3000;              // 超过该时常（单位ms），判断可能有连续水流或异物遮挡
bool COUNT_MODE = false;                      // 计数还是测速

int main(void){
  init();
  
  /********全局变量********/
  int n = 0;                                    // 水滴总数量
  int i = 0;                                    // 测速间隔内水滴数量
  int val_pin = 0;                              // 低电平灯亮；高电平，有东西灯灭
  const unsigned long begin_time = millis();    // 系统初始时间
  unsigned long temp_time = begin_time;         // 每次测速的初始时间
  unsigned long period_time = 0;                // 实际间隔运行时间ms
  int run_time = 0;                             // 总运行时间s  
  int speed;                                    // 流速：mL/h
  int avg_speed;                                // 平均流速：mL/h
  String unit;                                  // 显示的单位
  int factor;                                   // 流速单位转换系数
  
  //根据测量模式修改相关参数
  if (COUNT_MODE == false){
    unit = "mL/h";                       
    factor = 3600/HOW_MANY_DROPS;     
  }else{
      unit = "/min";
      factor = 60;
  }
  
  /******** setup ********/
  Serial.begin(9600);
  pinMode(COUNT_SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(SWITCH_GREEN_PIN, OUTPUT);

  /******** loop ********/
  while(1) {
    delay(10);
    /***每一滴计数***/
    val_pin = digitalRead(COUNT_SENSOR_PIN);    // 读取输入    
    if (val_pin == 1){                          // 光电传感器输出1
      unsigned long temp = millis();
      while(1){
        if (millis()-temp >= WARNING_PERIOD) {
          Serial.println("warning: Sensor Blocked!");
          Blink();
        }
        val_pin = digitalRead(COUNT_SENSOR_PIN); 
        if (val_pin == 0) break;                // 光电传感器接着输出0则为一次
        delay(10);
      }
      n = n+1;
      i = i+1;                                  // 水滴数加1
      Serial.println("num: " + String(i));
    }

    /***测速***/
    period_time = millis()-temp_time;
    if(period_time >= PERIOD){
      temp_time = millis();
      // Serial.println("PERIOD_NUM:" + String(i));//显示水滴数
      int temp = period_time/1000;              // 为了防止溢出，精确到每1s的滴数，而不是1ms
      speed = (i*factor)/temp;
      i = 0;
      if (speed < 0) {
        Serial.println("warning: Register Overflow!");
        Blink();
      }
      Serial.println("speed = " + String(speed) + unit);//显示流速
    }
    /***跳出循环的方法***/    
    if(Serial.read() == 'b') {
      run_time = (millis()-begin_time)/1000;    // 为了防止溢出，精确到每1s的滴数，而不是1ms
      avg_speed = (n*factor)/run_time;
      
      Serial.println("...ending...");
      Serial.println("total_run_time:" + String(run_time) + 's');//显示总运行时间
      Serial.println("avg_speed = " + String(avg_speed) + unit); //显示平均流速

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
    if(digitalRead(SWITCH_GREEN_PIN) == 0) {
      Serial.println("...go on...");
      break;
    }
  }
}