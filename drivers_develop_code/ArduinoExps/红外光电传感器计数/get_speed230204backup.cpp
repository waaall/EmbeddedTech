#include <Arduino.h>

/* 数据输出示例
SPEED = 36mL/h
SPEED = 36mL/h
SPEED = 36mL/h
SPEED = 0mL/h
SPEED = 0mL/h
SPEED = 324mL/h
SPEED = 864mL/h
SPEED = 1080mL/h
SPEED = 432mL/h
SPEED = 252mL/h
《关闭》
total_run_time:50s
AVG_SPEED = 306mL/h
*/

int main(void){
  init();
  
  /********需设置的量********/
  const int pin = 6;                            //光电传感器引脚
  const int how_many_drops = 20;                //1mL20滴液体
  const int periods = 5000;                     //测速间隔ms，不得小于1000ms
  const bool count_mode = true;                //计数还是测速
  
  /********全局变量********/
  int n = 0;                                    // 水滴总数量
  int i = 0;                                    // 测速间隔内水滴数量
  int val_pin = 0;                              // 低电平灯亮；高电平，有东西灯灭
  const unsigned long begin_time = millis();    //系统初始时间
  unsigned long temp_time = begin_time;         //每次测速的初始时间
  unsigned long periods_time = 0;               //实际间隔运行时间ms
  int run_time = 0;                             //总运行时间s  
  int speed;                                    //流速：mL/h
  int avg_speed;                                //平均流速：mL/h

  String unit = "/min";                         //显示的单位
  int factor = 60;                              //流速单位转换系数
  //根据测量模式修改相关参数
  if (count_mode == false){
    String unit = "mL/h";                       
    int factor = 3600/how_many_drops;     
  }
  
  /******** setup ********/
  Serial.begin(9600);
  pinMode(pin, INPUT);

  /******** loop ********/
  while(1) {
    /***每一滴计数***/
    val_pin = digitalRead(pin);      //读取输入
    if (val_pin == 1){               //光电传感器输出1
      while(1){
        val_pin = digitalRead(pin); 
        if (val_pin == 0) break;     //光电传感器接着输出0则为一次
      }
      n = n+1;
      i = i+1;                       //水滴数加1
    }
    /***测速***/
    periods_time = millis()-temp_time;
    if(periods_time >= periods){
      temp_time = millis();
      // Serial.println("periods_NUM:" + String(i));  //显示水滴数
      int temp = periods_time/1000;  //为了防止溢出，精确到每1s的滴数，而不是1ms
      speed = (i*factor)/temp;
      i = 0;
      Serial.println("SPEED = " + String(speed) + unit);//显示流速
    }
    delay(10);

    /***跳出循环的方法***/    
    if(Serial.read()=='b') {
      run_time = (millis()-begin_time)/1000;   //为了防止溢出，精确到每1s的滴数，而不是1ms
      avg_speed = (n*factor)/run_time;
      
      Serial.println("ending...")
      Serial.println("total_run_time:" + String(run_time) + 's');//显示总运行时间
      Serial.println("AVG_SPEED = " + String(avg_speed) + unit); //显示平均流速
 
      delay(2000);
      break;
    }
  }

  return 0;
}