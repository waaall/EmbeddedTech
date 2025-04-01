---
title: "stm32 硬件IIC使用方法说明与示例---LIS3DH的IIC通信_stm32 lis3dh-CSDN博客"
source: "https://blog.csdn.net/zhangfls/article/details/109078500"
author:
published:
created: 2025-03-30
description: "文章浏览阅读1w次，点赞9次，收藏67次。出于某些原因，我们可能需要MCU进行速率较高的IIC总线通信，一般stm32的IIC默认传输速率是100kpbs，最大为400kpbs。现在大部分项目会使用程序IO模拟的IIC，使用方便，具体网上例子很多。这里我需要使用LIS3DH三轴加速度传感器，获取三个方向的加速度用于碰撞检测。这个是LIS3DH数据刷新速率的配置寄存器：出于某些原因，我需要达到500hz以上的数据刷新速率,所以ODR要配置成0b1000，三轴芯片输出1.6khz速率的加速度信息。因为一条信息包含x、y、z个字节的数据，_stm32 lis3dh"
tags:
  - "clippings"
---
有时我们可能需要MCU进行速率较高的IIC总线通信，一般stm32的IIC默认传输速率是100kpbs，最大为400kpbs。现在大部分项目会使用程序IO模拟的IIC，使用方便，具体网上例子很多。

这里我需要使用LIS3DH三轴加速度传感器，获取三个方向的加速度用于碰撞检测

关于这个传感器的详细配置，可以参考这篇：

[https://blog.csdn.net/zhangfls/article/details/109021073](https://blog.csdn.net/zhangfls/article/details/109021073)

这个是LIS3DH加速度数据刷新速率的配置[寄存器](https://so.csdn.net/so/search?q=%E5%AF%84%E5%AD%98%E5%99%A8&spm=1001.2101.3001.7020)：

![](https://i-blog.csdnimg.cn/blog_migrate/23c3a6ac51799503655d30c0336fd750.png)

出于某些原因，我需要达到500hz以上的数据刷新速率,所以ODR要配置成0b1000，三轴芯片输出1.6khz速率的加速度信息。因为一条信息包含x、y、z个字节的数据，实际每读取一个方向的寄存器需要总计4次读写操作，所以总共至少12字节的通信才能完整获取到1次数据刷新。则通信的最小速率为1.6K\*12\*8=153600bps

开始我用IO模拟IIC读取，发现数据读不全，总有一部分数据被漏掉。网上查了一下，好像软件模拟IIC达不到这速率，所以只能考虑一下用stm32的硬件IIC，据说能到400Kbps。

这里用的是STM32F105RCT6,与LIS3DH三轴加速度传感器进行IIC通讯，获取三个方向的加速度用于碰撞检测。

示例：stm32F1的IIC配置都差不多

一、IIC初始化：

```cpp
void IIC1_Init()

{

    GPIO_InitTypeDef GPIO_InitStruct;

    I2C_InitTypeDef I2C_InitStruct;

    

    RCC_APB1PeriphClockCmd(RCC_APB1Periph_I2C1,ENABLE);

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);

 

    //GPIO配置

    GPIO_InitStruct.GPIO_Mode=GPIO_Mode_AF_OD;

    GPIO_InitStruct.GPIO_Pin=GPIO_Pin_6|GPIO_Pin_7;

    GPIO_InitStruct.GPIO_Speed=GPIO_Speed_50MHz;

    GPIO_Init(GPIOB,&GPIO_InitStruct);

    

    //IIC配置

    I2C_InitStruct.I2C_Ack=I2C_Ack_Enable;

    I2C_InitStruct.I2C_AcknowledgedAddress=I2C_AcknowledgedAddress_7bit;

    I2C_InitStruct.I2C_ClockSpeed=400000;

    I2C_InitStruct.I2C_DutyCycle=I2C_DutyCycle_2;

    I2C_InitStruct.I2C_Mode=I2C_Mode_I2C;

    I2C_InitStruct.I2C_OwnAddress1=0x55;

    I2C_Init(I2C1,&I2C_InitStruct);

    
    I2C_Cmd(I2C1,ENABLE);
}
```

二、IIC写一个字节寄存器（LIS3DH）

```cpp
void IIC_WriteByte(u8 addr,u8 data)

{

    u16 timeout=1000;

    I2C_AcknowledgeConfig(I2C1,ENABLE);

    I2C_GenerateSTART(I2C1,ENABLE);    //start

    while(!I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_MODE_SELECT))
    {
          if((timeout--)==0)
            {
                RS232_Printf(1,"EV5 Fail");
                break;
            }

    }    timeout=1000;

    

    I2C_Send7bitAddress(I2C1,LIS_ADDR|0x00,I2C_Direction_Transmitter);

    while(!I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED))

    {

          if((timeout--)==0)

            {

                RS232_Printf(1,"EV6 Fail");

                break;

            }

    }    timeout=1000;

    

    I2C_SendData(I2C1,addr);

    while(!I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_BYTE_TRANSMITTED))

    {

          if((timeout--)==0)

            {

                RS232_Printf(1,"EV8 Fail");

                break;

            }

    }    timeout=1000;

    

    I2C_SendData(I2C1,data);

    while(!I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_BYTE_TRANSMITTED))

    {

          if((timeout--)==0)

            {

                RS232_Printf(1,"EV8 Fail");

                break;

            }

    }    timeout=1000;

    

    I2C_GenerateSTOP(I2C1,ENABLE);

}
```

三、IIC读一个字节寄存器（LIS3DH）

```cpp
u8 IIC_ReadByte(u8 addr)

{

    u8 readtemp;

    u16 timeout=1000;

    

    I2C_AcknowledgeConfig(I2C1,ENABLE);

    

    I2C_GenerateSTART(I2C1,ENABLE);

    while(!I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_MODE_SELECT))

    {

          if((timeout--)==0)

            {

                RS232_Printf(1,"start Fail");

                break;

            }

    }    timeout=1000;

    

    I2C_Send7bitAddress(I2C1,LIS_ADDR|0x00,I2C_Direction_Transmitter);

    while(!I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED))

    {

          if((timeout--)==0)

            {

                RS232_Printf(1,"EV5 Fail");

                break;

            }

    }    timeout=1000;

    

    I2C_SendData(I2C1,addr);

  while(I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_BYTE_TRANSMITTED) != SUCCESS )

  {

          if((timeout--)==0)

            {

                RS232_Printf(1,"EV8 Fail");

                break;

            }

    }    timeout=1000;

    

    I2C_GenerateSTART(I2C1,ENABLE);

    while(!I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_MODE_SELECT))

    {

          if((timeout--)==0)

            {

                RS232_Printf(1,"start Fail");

                break;

            }

    }    timeout=1000;

    

    I2C_Send7bitAddress(I2C1,LIS_ADDR|0x01,I2C_Direction_Receiver);

    while(!I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_RECEIVER_MODE_SELECTED))

    {

          if((timeout--)==0)

            {

                RS232_Printf(1,"EV5 Fail");

                break;

            }

    }    timeout=1000;

    

    I2C_AcknowledgeConfig(I2C1,DISABLE);

  while(I2C_CheckEvent(I2C1,I2C_EVENT_MASTER_BYTE_RECEIVED) != SUCCESS )

  {

          if((timeout--)==0)

            {

                RS232_Printf(1,"ack Fail");

                break;

            }

    }    timeout=1000;

    

  readtemp = I2C_ReceiveData(I2C1);

    

  I2C_GenerateSTOP(I2C1,ENABLE);

  

  return readtemp;

}
```

四、LIS3DH初始化与数据读取

```cpp
uint8_t LIS3DH_Init(void)

{

    u8 res = 0;

    

    IIC1_Init();

    

    res = IIC_ReadByte(WHO_AM_I);

    if(res != 0x33)

    {

        return 0;

    }

 

    //测试FIFO

   IIC_WriteByte(LIS3DH_CTRL_REG1,0x80|0x0F);   //0010 0111    低功耗模式

    IIC_WriteByte(LIS3DH_CTRL_REG2,0x00);                //高通滤波关闭

 

    IIC_WriteByte(LIS3DH_CTRL_REG3,0x06);                //使能FIFO中断    0000 0110

    IIC_WriteByte(LIS3DH_CTRL_REG4,0x00);                //分辨率+-16g         0011 0000

 

    IIC_WriteByte(LIS3DH_CTRL_REG5,0x48);                    //FIFO使能    0100 1000

    IIC_WriteByte(LIS3DH_FIFO_CTRL,0x80|0x1D);        //0100 1111    配置FIFO模式和水印

    

    IIC_ReadByte(LIS3DH_INT1_SRC);    //清除中断位

    

    collect_LIS_Data();

    

    return 1;

}

 

 

void collect_LIS_Data(void)

{

        uint16_t  LIS_temp_data[3] = {0,0,0};

        uint8_t data_len,i;

 

        FIFO_data_len = IIC_ReadByte(LIS3DH_FIFO_SRC);

        

//        if(FIFO_data_len<0x40)

//                    return;

 

        FIFO_data_len &= 0x1F;

        for(i=0;i<FIFO_data_len;i++)

        {

            LIS3DH_ReadData(LIS_temp_data);

        }

}
```

上面的示例，将输出配置为FIFOstream模式，同时将速率配置成了1.6khz,watermarker配置成了29。

实测在主程序中，每10ms调用一次数据采集，每次读到的确实大约在15-17个之间，watermarker没有发生溢出。IIC通讯也没有把MCU的10ms全抢占完，其他任务运行也是正常的。基本可以确定stm32硬件IIC可以达到这样的速率。

另外，网上有一些说法，stm32的硬件IIC有BUG，长时间运行会崩溃之类的。我特意将设备挂了1天，到结束时，数据依旧可以正常接收，mcu也没有发生复位之类的问题

可能是ST已经修复了这个问题，也可能是我试的不够多，所以要使用的话最好还是要谨慎一些