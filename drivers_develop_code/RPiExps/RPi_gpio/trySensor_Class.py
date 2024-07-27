import RPi.GPIO as GPIO
import time
import sys
 
class Counting_Sensor():
    """docstring for Counting_Sensor"""
    def __init__(self, out_pin = 11, BCM = 0):
        super(Counting_Sensor, self).__init__()
        self.count = 0
        self.out_pin = out_pin
        self.BCM = BCM

        if self.out_pin < 0 or self.out_pin > 30:
            raise Exception('input wrong out_pin_number')
        if self.BCM != 0 and self.BCM != 1:
            raise Exception('input wrong code_number')

    def set_up(self):
        # 采用物理编码, BCM GPIO17的物理编码是11
        if self.BCM == 0:
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.out_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.out_pin, GPIO.BOTH, callback=self.detect_rsp, bouncetime=20)

    # 定义回调函数
    def detect_rsp(self, pin):
        print("detect\n")
        if GPIO.input(pin):
            print("物体遮挡")
            self.count += 1

    def loop(self):
        while True:
            # print(GPIO.input())
            # time.sleep(0.02)
            pass

    def clean(self):
        GPIO.cleanup()

# ===================main_function================== #

def main():
    drop = Counting_Sensor()
    drop.set_up()
    try:
        drop.loop()
    except KeyboardInterrupt:
        print(f"\n\ttotal_nums = {drop.count}\n")
        drop.clean()


if __name__ == '__main__':
    main()
