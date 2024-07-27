import RPi.GPIO as GPIO
import time


#/******** 需设置的参数（常量） ********/
COUNT_SENSOR_PIN = 13;              # 光电传感器引脚
LED_PIN = 15;                       # LED正极引脚
HOW_MANY_DROPS = 20;                # 1mL20滴液体
PERIOD = 5.0;                       # 测速间隔s
WARNING_PERIOD = 3.0;               # 超过该时常（单位s），判断可能有连续水流或异物遮挡
COUNT_MODE = False;                 # 计数还是测速



#/******** 函数：初始化 ********/
unit = "/min";                      # 显示的单位
factor = 60;                        # 流速单位转换系数

def Setup():
    # 根据测量模式修改相关参数
    global unit
    global factor
    if (COUNT_MODE == False):
        unit = "mL/h";                       
        factor = 3600/HOW_MANY_DROPS;       
    # 设置GPIO引脚模式
    GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
    GPIO.setup(COUNT_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(LED_PIN, GPIO.OUT) 



#/******** 函数：计数/测速 ********/
def Get_Speed():
    n = 0;                          # 水滴总数量
    i = 0;                          # 测速间隔内水滴数量
    val_pin = 0;                    # 低电平灯亮；高电平，有东西灯灭
    begin_time = time.time();       # 系统初始时间
    temp_time = begin_time;         # 每次测速的初始时间
    period_time = 0.0;              # 实际间隔运行时间ms
    run_time = 0.0;                 # 总运行时间s  
    speed = 0.0;                    # 流速：mL/h
    avg_speed = 0.0;                # 平均流速：mL/h

    #/***每一滴计数***/
    try:
        while True:
            time.sleep(0.01)
            if (GPIO.input(COUNT_SENSOR_PIN) == 1):
                temp = time.time()
                while True:
                    # 遮挡时间过长报错
                    if (time.time()-temp >= WARNING_PERIOD) :
                        print("warning: Sensor Blocked!\n")
                        Blink()
                    # 光电传感器接着输出0则为一次
                    if (GPIO.input(COUNT_SENSOR_PIN) == 0):
                        break
                    time.sleep(0.01)
    
                n = n+1
                i = i+1
                print(f"Num: {i}\n")   
    
            #/***测速***/
            period_time = time.time()-temp_time
            if (period_time >= PERIOD) :
                speed = (i*factor)/period_time
                temp_time = time.time()
                i = 0
                if (speed < 0) :
                    print("warning: Register Overflow!\n")
                    Blink()
                print(f"speed = {speed} {unit}\n")# 显示流速
        
    except KeyboardInterrupt:
        run_time = (time.time()-begin_time)/1000  # 为了防止溢出，精确到每1s的滴数，而不是1ms
        avg_speed = (n*factor)/run_time
    
        print("...ending...\n")
        print(f"total_run_time: {run_time}s\n")# 显示总运行时间
        print(f"avg_speed = {avg_speed} {unit}\n")# 显示平均流速

        time.sleep(1)


#/******** 函数：LED闪烁 ********/
def Blink():
    try:
        while True:
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED_PIN,GPIO.LOW)
            time.sleep(0.5)

    except KeyboardInterrupt: 
        print("\ncontinue...\n")


def Destroy():
    GPIO.cleanup()



#/******** main函数 ********/
if __name__ == '__main__':     
    Setup()
    try:
        Get_Speed()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, destroy() will be executed
        Destroy()