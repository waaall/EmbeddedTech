#include <iostream>
#include <gpiod.hpp>


int main(){

    //创建一个 gpiod::chip对象，用于访问制定的GPIO控制器
    gpiod::chip chip("gpiochip0");
    //获取控制器gpiochip0中编号5的gpio端口
    auto line = chip.get_line(17);
    //
    line.request({"test", gpiod::line_request::EVENT_BOTH_EDGES, 1});


    for(;;){
        auto event = line.event_wait(std::chrono::nanoseconds(100000));
        if (event){
            std::cout << "signal_changed" << std::endl;
        }
    }

    //释放申请的GPIO端口
    line.release();

    return 0;
}