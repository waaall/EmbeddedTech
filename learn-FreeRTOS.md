
## Reference
- [Free RTOS github](https://github.com/FreeRTOS/FreeRTOS)
- [free RTOS doc](https://wwww.freertos.org/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals)
- [freeRTOS doc zh](https://wwww.freertos.org/zh-cn-cmn-s/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals)

- [CMSIS-RTOS2](https://arm-software.github.io/CMSIS_6/latest/RTOS2/index.html)


## RTOS 基本概念

### Free RTOS 和 CMSIS-RTOS2

- [FreeRTOS与CMSIS标准](https://doc.embedfire.com/linux/stm32mp1/freertos/zh/latest/application/freertos%26cmsis.html)
- [CMSIS-RTOS 和 freertos 论坛](https://forum.anfulai.cn/forum.php?mod=viewthread&tid=27356&amp;fpage=2)
市面上RTOS的种类很多，除了FreeRTOS还有uCOS、RTX、RT-thread等等，每个RTOS操作系统都有自己的API接口， 它们的内核组件功能都是类似的，ARM公司为了统一操作系统、降低嵌入式开发的门槛提供了CMSIS-RTOS， CMSIS-RTOS将各个RTOS的接口统一起来，提供CMSIS-RTOS的接口供使用者使用，从而提高代码的移植性以及开发效率。

#### CMSIS 架构简介
CMSIS标准中最主要的为CMSIS核心层，它包括了：
- 内核函数层：其中包含用于访问内核寄存器的名称、地址定义，主要由ARM公司提供。
- 设备外设访问层：提供了片上的核外外设的地址和中断定义，主要由芯片生产商提供。
- CMSIS实时系统API层: 封装并统一了各个实时操作系统的内核操作接口，主要由ARM公司提供。
CMSIS层位于硬件层与操作系统或用户层之间，提供了与芯片生产商无关的硬件抽象层， 可以为接口外设、实时操作系统提供简单的处理器软件接口，屏蔽了硬件差异，这对软件的移植是有极大的好处的。

##### CMSIS-RTOS架构

![](learn-FreeRTOS.assets/cmsis_rtos2_overview.png)
Many popular RTOS kernels include support for CMSIS-RTOS2 API:

**CMSIS-RTX** (or Keil RTX5): provides most complete support for CMSIS-RTOS2 API and uses it as native interface. For more information see:
- [CMSIS-RTX GitHub repository](https://github.com/ARM-software/CMSIS-RTX)
- [CMSIS-RTX documentation](https://arm-software.github.io/CMSIS-RTX/)
- [CMSIS-RTX pack](https://www.keil.arm.com/packs/cmsis-rtx-arm/versions/)

**FreeRTOS** : this popular RTOS kernel is enabled with CMSIS-RTOS2 API in the _CMSIS-FreeRTOS_ variant. To learn more see:
- [CMSIS-FreeRTOS GitHub repository](https://github.com/ARM-software/CMSIS-FreeRTOS)
- [CMSIS-FreeRTOS documentation](https://arm-software.github.io/CMSIS-FreeRTOS/)
- [CMSIS-FreeRTOS pack](https://www.keil.arm.com/packs/cmsis-freertos-arm/versions/)

**Zephyr RTOS**: is developed under governance of Linux Foundation and includes CMSIS-RTOS2 API support. See more at:
- [Zephyr GitHub repository](https://github.com/zephyrproject-rtos/zephyr), see folder _subsys/portability/cmsis_rtos_v2/_
- [Zephyr documentation about CMSIS-RTOS2 support](https://docs.zephyrproject.org/latest/services/portability/cmsis_rtos_v2.html)

**embOS**: is a preemptive RTOS designed by Segger, and provides support for CMSIS-RTOS2 API.
- [Using embOS in CMSIS-Pack projects](https://wiki.segger.com/Using_embOS_in_CMSIS-Pack_projects)
- [CMSIS-embOS pack](https://www.keil.arm.com/packs/cmsis-embos-segger/versions/)

**Azure ThreadX RTOS for STM32**: is an integration of Azure RTOS into STM32 middleware provided by STMicroelectronics.
- [CMSIS-RTOS API support in ThreadX for STM32](https://wiki.st.com/stm32mcu/wiki/Introduction_to_THREADX#CMSIS-RTOS_API_Support)

**Micrium OS** is developed and maintained by Silicon Labs.
- [Micrium OS overview and comparison](https://www.silabs.com/developers/rtos)


## freertos 学习路线

- [freertos 中文官方文档 - RTOS 基础知识](https://www.freertos.org/zh-cn-cmn-s/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals)

学习 FreeRTOS 建议走两条线并行：一条是把内核机制吃透，另一条是跟着成熟开源工程学工程化做法。

### 一、学习路线

1. 先跑[官方 Demo](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)，再[对照源码](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo)读机制
    FreeRTOS 官方有“Demo Applications”说明页，告诉你不同平台 Demo 的位置和注意事项；同时经典的 FreeRTOS 打包仓库里也包含大量现成示例工程（很多以子模块形式引入内核与库）。
    
2. 把最核心的并发原语按场景掌握
    任务与调度（优先级、时间片、阻塞）、队列、任务通知、信号量与互斥量（优先级继承）、事件组、软件定时器、Stream/Message Buffer、ISR 里该用哪些 FromISR API。读[内核仓库](https://github.com/FreeRTOS/FreeRTOS-Kernel)时重点看 portable 层、task/queue/timers 的实现和配置项。
    
3. 在 PC 上做“可调试”的练习
    用 [FreeRTOS 的 Linux/Posix](https://freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux) 仿真 Demo 在 PC 上跑任务、打断点、看栈和时序，学习成本低，迭代快。
    
4. 工程化必做的三项训练
    内存与栈：开启栈水位检查，统一栈大小估算和监控
    时序：为关键任务定义周期、deadline、阻塞点，避免忙等
    ISR 设计：ISR 只做最小化工作，借助队列/通知把重活交给任务

### 二、相关的开源项目

#### FreeRTOS 官方家族

- FreeRTOS-Kernel（内核与各平台移植层）：学习“内核与移植层解耦”的结构、portmacro 与临界区实现、“用配置裁剪功能”的思路。

- FreeRTOS/FreeRTOS（经典发行版）：学习“内核 子库 Demo 工程”如何组织、如何用子模块管理多仓库依赖。

 - FreeRTOS-Plus-TCP：学习轻量 TCP/IP 栈如何做可裁剪内存、Socket 风格 API、网络任务与应用任务的边界。

- Lab-Project-FreeRTOS-FAT（FreeRTOS+FAT）：学习线程安全文件系统的锁策略、标准/原生 API 的取舍、与网络例程的集成方式。

#### 物联网库

- [coreMQTT](https://github.com/FreeRTOS/coreMQTT)：非常适合学习“平台无关核心库 适配层接口”的写法，它几乎只依赖标准 C 和你实现的网络传输接口，目标是低内存占用。

- coreMQTT-Agent-Demos：学习多任务共享一条 MQTT 连接的模式，把同步复杂度封装进 Agent/守护任务里，应用层更简单。

#### 芯片厂 SDK

- [ESP-IDF](https://github.com/espressif/esp-idf) & [ESP-IDF（doc）](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos.html)：大量组件和应用基于 FreeRTOS，文档明确说明其把 FreeRTOS 作为系统组件集成，并且为多核目标提供了特定实现（SMP 等），很适合学事件循环、组件化、任务划分与资源管理。

- STM32 的 FreeRTOS 中间件组件仓库（[stm32-mw-freertos](https://github.com/STMicroelectronics/stm32-mw-freertos)）：适合学习“厂商对上游 FreeRTOS 的封装方式”、以及和 Cube 生态协作的目录与发布策略。

- [NXP MCUXpresso SDK](https://github.com/nxp-mcuxpresso/mcux-sdk) 与 examples：适合学习“从板级到应用”的分层和示例工程组织方式，很多工程会展示 RTOS 与驱动、中间件的组合打法。

