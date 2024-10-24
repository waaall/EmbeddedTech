
「转载」

# 目录
[1、STM32CubeMX操作](https://blog.csdn.net/tangxianyu/article/details/121138328#t0 "1、STM32CubeMX操作")
[2、程序完善](https://blog.csdn.net/tangxianyu/article/details/121138328#t1 "2、程序完善") 
[3、MODBUS SLAVE程序的移植](https://blog.csdn.net/tangxianyu/article/details/121138328#t2 "3、MODBUS SLAVE程序的移植")
	 [3.1程序下载和复制](https://blog.csdn.net/tangxianyu/article/details/121138328#t3 "3.1程序下载和复制")
	 [3.2程序添加，编译](https://blog.csdn.net/tangxianyu/article/details/121138328#t4 "3.2程序添加，编译")
	 [3.3接口替换](https://blog.csdn.net/tangxianyu/article/details/121138328#t5 "3.3接口替换")
	 [3.4修改main.c主函数](https://blog.csdn.net/tangxianyu/article/details/121138328#t6 "3.4修改main.c主函数")
[4、MODBUS调试](https://blog.csdn.net/tangxianyu/article/details/121138328#t7 "4、MODBUS调试")
[5. 总结](https://blog.csdn.net/tangxianyu/article/details/121138328#t8 "5. 总结")

# 1. STM32CubeMX操作

## 1.1 新建工程

打开STM32CubeMX软件，File-->New Project。新建工程。

![](https://i-blog.csdnimg.cn/blog_migrate/5f95cd68578c567a34c49db1b9d65e3b.png)

 在打开的对话框内，在1处的Part Number文本框内输入STM32F103ZE，会在2处自动产生可以选择的芯片，在这里选择LQFP144封装的STM32F103ZETx系列的芯片。

![](https://i-blog.csdnimg.cn/blog_migrate/e00889962ea734b3230fbf0641ea51fd.png)

## 1.2芯片配置

### 1.2.1 时钟配置

进入芯片配置界面，首先选择System Core选项下面的RCC，然后在弹出的High Speed Clock选项下选择Crystal/Ceramic Resonator。

![](https://i-blog.csdnimg.cn/blog_migrate/4ac2cc76e80146e4264adb016005e708.png)

 点击3处的Clock Configuration，在弹出的界面，在1处输入输入72，系统会自动将其他的时钟调整为相对应的配置。

![](https://i-blog.csdnimg.cn/blog_migrate/18c4f3fffccd26c1a14f16e91486a6fa.png)

为了使生成的程序可以进行在线调试，重新点击1处的Pinout&Configuration，点击SYS，在Debug处点击Serial Wire。

### 1.2.2 串口的配置
![](https://i-blog.csdnimg.cn/blog_migrate/c06115ac925da354e528ac3a39e9d083.png)

在Pinout&Configuration选项卡下，选择Connectctivity下的UART4(可以根据自己的电路板的实际接口进行选择)，Mode选择Asynchronous（异步模式）。![](https://i-blog.csdnimg.cn/blog_migrate/85fca41d8d54431dd4a780e1afa4b4a5.png)

 **首先进行参数配置（Parameter Settings）**：

Basic Parameters:

        Baud：                115200bit Bits/s        波特率

        Word Length:       8Bits                        字长

        Parity:                None                        无校验

        Stop Bits:        1                        1位停止位

Advanced Parameters:

        Data Direction:        Receive and Transmit                既接收也发送

        Over Sampling：        16 Samples

**其次进行User Constant配置：**

此项参数不变

**再次进行NVIC setting配置：**

此处将UART4 global interrupt进行使能，优先级等后续再进行配置。

![](https://i-blog.csdnimg.cn/blog_migrate/1f8c48354b9f58e803b5eb61f2c24a57.png)

**DMA和GPIO配置不用更改。**

### **1.2.3 定时器的配置**

在modbus中，需要判断一帧什么时候发送结束，我们采用定时器进行判断。当定时器时间大于我们设定的时间时，发生定时器中断，告诉系统，一帧数据发送完成。

首先选择TIM7下的Parameter Settings，将PSC设置为7199，Counter Mode设置为UP，Counter Period 设置为39，Auto-reload preload设置为Enable。

在中断开启的情况下，中断时间为：

![\frac{7200*40}{72,000,000}=4ms](https://latex.csdn.net/eq?%5Cfrac%7B7200*40%7D%7B72%2C000%2C000%7D%3D4ms)

即超过4ms仍旧没有数据发送过来，证明一帧数据发送完成。

![](https://i-blog.csdnimg.cn/blog_migrate/0d266e18161d92b7aa777b98cdf60675.png)

开启定时器的NVIC中断，即TIM7 global interrupt更改为Enable，此处优先级先不进行设置，等后续在NVIC中集中进行设置。

![](https://i-blog.csdnimg.cn/blog_migrate/5538eba603cf85c35f64de40f930c7f7.png) 

### 1.2.4 NVIC配置

在System Core选项下，选择NVIC，在NVIC的选项下，将Priority Group优先级分组设置为2位为pre-emption priority, 2位为subpriority。

然后将UART4的优先级设置为3,3低于TIM7的优先级3,2。证明当串口中断和时间中断同时来的时候，先相应时间中断。

![](https://i-blog.csdnimg.cn/blog_migrate/9318576f8c614e50df3d97c3365d5cdd.png)

### 1.2.5 工程设置

选择最上面的Project Manager的Project，首先对新建的工程命名为ModbusSlave，将Application Structure更改为Basic，最后将开发工具改成自己的开发工具，我这里用的是KEIL，这里选择MDK。

![](https://i-blog.csdnimg.cn/blog_migrate/eb7fdd1ad132735eb2537112d569e24e.png)

然后选择Code Generator，在这个界面将Generator peripheral initalization as a pair of '.c/.h' files per peripheral前面勾选上。

![](https://i-blog.csdnimg.cn/blog_migrate/400bbfa35aace2f58a1510569e0436e1.png)

最后生成代码：

![](https://i-blog.csdnimg.cn/blog_migrate/65db621a21f74ee7a697ddcc6f4cd788.png)

#  2、程序完善

## 2.1完善usart.h

为了确保在更新STM32CubeMX的时候，我们自己增加的程序不会被删除掉。我们在完善程序的时候需要将程序增加到制定的位置。例如在usart.h内的，我们将需要增加的程序到：

```c
/* USER CODE BEGIN Private defines */
 
/* USER CODE END Private defines */
```

首先定义一个UART\_BUF结构体，里面包含接收的缓冲数据和大小，以及发送的数据集大小。

然后定义一个串口的初始化函数E\_USART\_INIT来对定义的UART\_BUF进行初始化。定义一个串口中断回调函数HAL\_UART\_RxCpltCallback.

![](https://i-blog.csdnimg.cn/blog_migrate/4b2518ff5b57e78e4f0432ddea5928fb.png)

```c
/* USER CODE BEGIN Private defines */
typedef struct
{
	uint8_t *rx_buf;		//接收缓冲数组
	uint16_t rx_buf_cnt;	//接收缓冲计数值
	uint16_t rx_size;		//接收数据大小
	uint8_t rx_flag;		//接收完成标志位
	
	uint8_t *tx_buf;		//发送缓冲数组
	uint16_t tx_buf_cnt;	//发送缓冲计数值
	uint16_t tx_size;		//实际发送数据大小
}UART_BUF;					//串口结构体
 
extern UART_BUF uart4;		//串口结构体实体
/* USER CODE END Private defines */
 
void MX_UART4_Init(void);
 
/* USER CODE BEGIN Prototypes */
void E_USART_INIT(UART_HandleTypeDef *huart);
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);
 
/* USER CODE END Prototypes */

```

##  2.2完善usart.c

### 2.2.1头文件完善

在/\*USER CODE BEGIN 0\*/和/\*USER CODE END 0\*/中间添加完善程序

```c
/* USER CODE BEGIN 0 */
#include "string.h"
#include "tim.h"
#define UART4_RXSIZE	1024	//一帧接收数据的最大值
#define UART4_TXSIZE	1024	//一帧发送数据的最大值
 
uint8_t uart4_rx_buf[UART4_RXSIZE];	//发送数据缓冲数组
uint8_t uart4_tx_buf[UART4_TXSIZE];	//接收数据缓冲数据
 
UART_BUF uart4;			//串口结构体实体
uint8_t RxBuffer;		//接收数据中间变量
/* USER CODE END 0 */

```

### 2.2.2增加回调函数

在/\* USER CODE BEGIN 1 \*/和/\* USER CODE END 1 \*/增加回调函数HAL\_UART\_RxCpltCallback。

基本原理为接收到一个数据调用回调函数（RxBuffer），然后将数据赋值给rx\_buf这个数组，然后清除定时器的计数，重新开始计数，防止定时器产生中断。

```c
/*****************************重写回调函数，实现串口数据接收**********************/
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	if(huart->Instance == UART4)
	{
		if(uart4.rx_buf_cnt >= UART4_RXSIZE-1)	//接收数据量超限，错误
		{
			uart4.rx_buf_cnt = 0;
			memset(uart4.rx_buf, 0x00, sizeof(uart4.rx_buf));
			HAL_UART_Transmit(huart, (uint8_t *)"数据溢出", 10, 0xFFFF);		
		}
		else									//接收正常
		{
			uart4.rx_buf[uart4.rx_buf_cnt++] = RxBuffer;	//接收数据存储到rx_buf
			HAL_TIM_Base_Stop_IT(&htim7);
			__HAL_TIM_SET_COUNTER(&htim7, 0);
			HAL_TIM_Base_Start_IT(&htim7);		//将定时器7的计数值清零后重新计数
		}
		HAL_UART_Receive_IT(huart, (uint8_t *)&RxBuffer, 1);
	}
}

```

### 2.2.3串口初始化函数

在回调函数下方增加串口参数初始化函数E\_USART\_INIT

```c
/*****************************对UART_BUF结构体的实体uart4赋值**********************/
void E_USART_INIT(UART_HandleTypeDef *huart)
{
	if(huart->Instance == UART4)
	{
		uart4.rx_buf = uart4_rx_buf;	//接收数据变量初始化
		uart4.rx_buf_cnt = 0;
		uart4.rx_size = 0;
		uart4.rx_flag = 0;
		
		uart4.tx_buf = uart4_rx_buf;	//发送数据变量初始化
		uart4.tx_buf_cnt = UART4_TXSIZE;
		uart4.tx_size = 0;		
		
		HAL_UART_Receive_IT(huart, uart4.rx_buf, 1);	//开启接收中断
	}
 
}

```

在初始化过程中最后一句话是开启中断，让每接收一个数据进入一次回调函数。

## 2.3完善tim.h

增加在tim.c中的函数声明，在/\* USER CODE BEGIN Prototypes \*/和/\* USER CODE END Prototypes \*/中间增加：

```c
/* USER CODE BEGIN Prototypes */
void E_TIM_INIT(TIM_HandleTypeDef *htim);
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim);
/* USER CODE END Prototypes */

```

## 2.4完善tim.c

### 2.4.1完善头文件

在头文件增加一个函数引用

```c
/* USER CODE BEGIN 0 */
#include "usart.h"
/* USER CODE END 0 */

```

###  2.4.2完善回调函数和初始化函数

在/\* USER CODE BEGIN 1 \*/和/\* USER CODE END 1 \*/内部增加时间回调函数和时间初始化函数。具体含义已在注释内说明，此处不赘述。

```c
/* USER CODE BEGIN 1 */
/*****************************重写时间回调函数**********************/
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
	if(htim == &htim7)
	{
		__HAL_TIM_CLEAR_FLAG(&htim7, TIM_FLAG_UPDATE);	//产生中断证明超过4ms没有接收到数据了，一帧接收完成
		HAL_TIM_Base_Stop_IT(&htim7);		//中断之后停止定时器，开启在下一次接收到数据开始
		uart4.rx_size = uart4.rx_buf_cnt;	//将接收到数据数量赋值
		uart4.rx_buf_cnt = 0;				//清零
		uart4.rx_flag = 1;					//接收完成，置1
	}
 
}
 
void E_TIM_INIT(TIM_HandleTypeDef *htim)
{
	if(htim == &htim7)
	{
		__HAL_TIM_CLEAR_FLAG(htim, TIM_FLAG_UPDATE);		//手动添加
		HAL_TIM_Base_Start_IT(htim);
	}
 
}
 
/* USER CODE END 1 */

```

## 2.5完善main.c

上面的函数完善都是为了处理数据发送和接收的函数，通过以上处理可以完成数据的发送和接受。在移植MODBUS函数之前可以对数据发送和接受是否正常进行测试。此处的main.c就是完成数据的转发功能，即接收到什么数据就向外转发什么数据。

首先在  /\* USER CODE BEGIN 2 \*/和  /\* USER CODE END 2 \*/内部增加定时器和串口的初始化函数

```c
  /* USER CODE BEGIN 2 */
	E_USART_INIT(&huart4);
	E_TIM_INIT(&htim7);
  /* USER CODE END 2 */

```

然后再在主函数的while循环内增加程序：

```c
  while (1)
  {
    /* USER CODE END WHILE */
	  
    /* USER CODE BEGIN 3 */
	  // 此处是用来测试收啥发啥的。	  
	  if(uart4.rx_flag == 1)	//如果一帧数据接收完成，其在tim7的回调函数置位
	  {
		HAL_UART_Transmit(&huart4, (uint8_t *)(uart4.rx_buf), uart4.rx_size, 500);//向外转发收到的数据
		while(__HAL_UART_GET_FLAG(&huart4,UART_FLAG_TC)!=SET);	//死循环等待
		uart4.rx_buf_cnt = 0;									//计数值清零
		uart4.rx_flag=0;										//接收完成标志位清零
	  }
	  
	  HAL_Delay(5);		//每间隔5ms循环一次
  }
  /* USER CODE END 3 */
}

```

## 2.6调试

### 2.6.1KEIL的设置

为了确保每次程序下载完成后后自动复位运行，需要对KEIL进行的debug进行设置，设置步骤如下：将Reset and Run前面的√点上。

![](https://i-blog.csdnimg.cn/blog_migrate/9f208a64f0bfd3dd4beb67ef7962dcf4.png)

 ![](https://i-blog.csdnimg.cn/blog_migrate/14b72e8f78064d108048281203a2b6a7.png)

![](https://i-blog.csdnimg.cn/blog_migrate/099ce92860c4534d131f9234af3f8efa.png)

###  2.6.2程序下载调试

编译无误后将程序下载到电路板中，然后将电路板的UART4的串口与电脑口相连。打开串口调试助手，按照程序在串口调试助手内进行相应配置。

![](https://i-blog.csdnimg.cn/blog_migrate/4f28c7cf352d97bb91c654d721ec2557.png)

配置完成之后，打开串口就可以进行数据发送接收了。

![](https://i-blog.csdnimg.cn/blog_migrate/f6dafaae7d739060663eee299b210ee5.png)


# 3、MODBUS SLAVE程序的移植

##  3.1程序下载和复制

在[https://download.csdn.net/download/tangxianyu/37014694](https://download.csdn.net/download/tangxianyu/37014694 "https://download.csdn.net/download/tangxianyu/37014694")地址下载modbus-slave（RTU）程序，解压后分别将已经编写好的modbus.c和modbus.h分别复制到Src和Inc文件夹内

![](https://i-blog.csdnimg.cn/blog_migrate/5cec6b284611cd446de249dd938e891a.png)

![](https://i-blog.csdnimg.cn/blog_migrate/53be65ad85cf008c458cc3bb909d0efb.png) 

##  3.2程序添加，编译

将modbus.c文件加入到工程当中，具体步骤如下图所示，不赘述。

![](https://i-blog.csdnimg.cn/blog_migrate/20762ba278a205fc81b19280942d3edf.png)

![](https://i-blog.csdnimg.cn/blog_migrate/aead3b8688a578cbc4e998dc5d5e7a9e.png)

 添加完成之后点击编译，此时会发现有很多错误，不用理会错误。我们可以发现modbus.h也同样显示出来了。 

## 3.3接口替换

打开modbus.c文件，将修改顶部的宏定义：如果用到的串口是UART4那么宏定义文件可以不变，如果不是将串口改成相应的接口就可以。

```c
#include "Modbus.h"
#include "string.h"
 
#define MODBUS_UART uart4			//将串口改成相应的变量即可，例如用到UART1，此处改为uart1
#define MODBUS_HUART huart4			//将串口改成相应的变量即可，例如用到UART1，此处改为huart1
```

## 3.4修改main.c主函数

在头文件内加入modbus.h

![](https://i-blog.csdnimg.cn/blog_migrate/4c883a3ac6d486c996ef5f9a8cdc1895.png)

 将之前的死循环内的函数修改：

![](https://i-blog.csdnimg.cn/blog_migrate/b65b3f7491512a65c6b1cb34bad2ce56.png)

 至此，MODBUS-SLAVE函数修改完成。下一步是调试。

# 4、MODBUS调试

这里用到的modbus调试工具为Modbus Poll，在CSDN中很容易搜索到，这里我就不放链接地址了。

打开 modbus Poll软件 -->Connection, 在弹出的对话框Connection Setup进行波特率等设置，设置好之后点击OK.

![](https://i-blog.csdnimg.cn/blog_migrate/70611e769204a60bf7a766e66d62a04b.png)

通讯数据如下：

![](https://i-blog.csdnimg.cn/blog_migrate/70ca04d7ac7177e00ab32e49908371cf.png)

通讯数据应该为0XAA55和0X55AA，此处显示的十进制数，需要进行转换一下。将Signed的数据类型，转换成Hex，则显示数据与我们的预期一致。

![](https://i-blog.csdnimg.cn/blog_migrate/77d30cae8250b0a3666469bfdd09a439.png)