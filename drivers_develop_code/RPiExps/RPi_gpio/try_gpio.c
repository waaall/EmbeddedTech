#include <gpiod.h>

// #define CHIP_NAME 

int gpio_setup(char* chip_name, int line_number, struct gpiod_chip * chip, struct gpiod_line * line){
    chip = gpiod_chip_open(chip_name);
    if (!chip) return -1;

    line = gpiod_chip_get_line(chip, line_number);
    if (!line) {
        gpiod_chip_close(chip);
        return -1;
    }

    return 0;
}


int main(){
    char* chip_name = "dev/gpiochip0";
    int line_number = 17;

    struct gpiod_chip * chip;
    struct gpiod_line * line;

    int set_status = gpio_setup(chip_name, line_number, chip, line);
    if (set_status < 0){
        printf("GPIO初始化错误");
        return -1;
    }

    int rv, value;
    rv = 

    return 0;
}