
- [CMSIS5官方文档](https://arm-software.github.io/CMSIS_5/General/html/index.html)
- [CMSIS6官方文档](https://arm-software.github.io/CMSIS_6/latest/General/index.html)

![](GD32-develop.assets/CMSIS-Overview.png)

|CMSIS-...|Target Processors|Description|
|:--|:--|:--|
|[**Core(M)**](https://arm-software.github.io/CMSIS_5/Core/html/index.html)|All Cortex-M, SecurCore|Standardized API for the Cortex-M processor core and peripherals. Includes intrinsic functions for Cortex-M4/M7/M33/M35P SIMD instructions.|
|[**Core(A)**](https://arm-software.github.io/CMSIS_5/Core_A/html/index.html)|Cortex-A5/A7/A9|Standardized API and basic run-time system for the Cortex-A5/A7/A9 processor core and peripherals.|
|[**Driver**](https://arm-software.github.io/CMSIS_5/Driver/html/index.html)|All Cortex|Generic peripheral driver interfaces for middleware. Connects microcontroller peripherals with middleware that implements for example communication stacks, file systems, or graphic user interfaces.|
|[**DSP**](https://arm-software.github.io/CMSIS_5/DSP/html/index.html)|All Cortex-M|DSP library collection with over 60 functions for various data types: fixed-point (fractional q7, q15, q31) and single precision floating-point (32-bit). Implementations optimized for the SIMD instruction set are available for Cortex-M4/M7/M33/M35P.|
|[**NN**](https://arm-software.github.io/CMSIS_5/NN/html/index.html)|All Cortex-M|Collection of efficient neural network kernels developed to maximize the performance and minimize the memory footprint on Cortex-M processor cores.|
|[**RTOS v1**](https://arm-software.github.io/CMSIS_5/RTOS/html/index.html)|Cortex-M0/M0+/M3/M4/M7|Common API for real-time operating systems along with a reference implementation based on RTX. It enables software components that can work across multiple RTOS systems.|
|[**RTOS v2**](https://arm-software.github.io/CMSIS_5/RTOS2/html/index.html)|All Cortex-M, Cortex-A5/A7/A9|Extends CMSIS-RTOS v1 with Armv8-M support, dynamic object creation, provisions for multi-core systems, binary compatible interface.|
|[**Pack**](https://arm-software.github.io/CMSIS_5/Pack/html/index.html)|All Cortex-M, SecurCore, Cortex-A5/A7/A9|Describes a delivery mechanism for software components, device parameters, and evaluation board support. It simplifies software re-use and product life-cycle management (PLM).   <br>Is part of the [**Open CMSIS Pack project**](https://www.open-cmsis-pack.org/).|
|[**Build**](https://arm-software.github.io/CMSIS_5/Build/html/index.html)|All Cortex-M, SecurCore, Cortex-A5/A7/A9|A set of tools, software frameworks, and work flows that improve productivity, for example with Continuous Integration (CI).  <br>Is replaced with the [**CMSIS-Toolbox**](https://github.com/Open-CMSIS-Pack/devtools/tree/main/tools).|
|[**SVD**](https://arm-software.github.io/CMSIS_5/SVD/html/index.html)|All Cortex-M, SecurCore|Peripheral description of a device that can be used to create peripheral awareness in debuggers or CMSIS-Core header files.|
|[**DAP**](https://arm-software.github.io/CMSIS_5/DAP/html/index.html)|All Cortex|Firmware for a debug unit that interfaces to the CoreSight Debug Access Port.|
|[**Zone**](https://arm-software.github.io/CMSIS_5/Zone/html/index.html)|All Cortex-M|Defines methods to describe system resources and to partition these resources into multiple projects and execution areas.|

# 一: 整体框架

make + arm-none-eabi-gcc完成arm的mcu的编译过程，不论是stm32或者GD32，都是类似的CMSIS、外设库函数、startup、和ld文件，这些文件都是干什么的，整个make + arm-none-eabi-gcc 的编译过程是怎么样的，哪些步骤需要哪些文件干什么？

ARM MCU（如STM32和GD32）的编译过程以及各个文件的作用。 当前的GD32项目结构，我来详细解释ARM MCU（STM32/GD32）的编译过程和各个文件的作用：

## 1. ARM MCU项目文件结构详解


### 1.1 CMSIS层（Cortex Microcontroller Software Interface Standard）

- **作用**: ARM公司制定的标准接口，提供硬件抽象层
- **主要文件**:
  - `core_cm4.h`: Cortex-M4内核定义
  - `xx32f4xx.h`: 寄存器、中断向量定义
  - `system_xx32f4xx.c`: 系统初始化函数


#### 1.1.2 xx32f4xx.h: 寄存器、中断向量定义

主要工作简介：
- 提供应用层 ISR 实现，名字必须与向量表中的符号一致，或通过别名/映射对齐
- 在 ISR 中清标志、读写外设寄存器，避免重复进中断

关键职责：
- 定义异常/中断函数：HardFault_Handler、SysTick_Handler、外设 ISR 等
- 调用驱动/HAL 的 IRQ 处理（如 HAL_TIM_IRQHandler）
- 提供声明头（xxx_it.h）让编译器正确链接用户 ISR

与 startup 的耦合：
- startup 提供 weak 的 ISR 符号；it 提供强定义覆盖
- 名字不对或顺序不匹配会导致：
  - 进了错误的 ISR（功能错乱）
  - 落到 Default_Handler（系统卡死）

STM32 vs GD32 常见差异：
- ISR 名称不同（如 TIM、USART、DMA、EXTI 的路由和编号）
- IRQn 枚举不同（影响 NVIC_EnableIRQ 的参数）

#### 1.1.3 system_32f4xx.c: 系统初始化函数

主要工作简介：
- 配置时钟树（HSE/HXTAL、HSI/IRC、PLL 分频/倍频），决定 SystemCoreClock
- 配置 Flash 等待周期（不同频率与电压域下的 LATENCY）
- 可选：Cache/ART/Prefetch、FPU 使能、总线时钟分频（AHB/APB）、某些电源/电压调节设置

关键职责：
- 提供 SystemInit：由 startup 调用，尽快把系统带到期望频率
- 维护 SystemCoreClock 全局变量及 SystemCoreClockUpdate 函数
- 芯片特定宏：STM32 常用 HSE_VALUE/HSI_VALUE；GD32 常用 HXTAL_VALUE/IRC16M_VALUE，并可能用编译期宏直接选择目标主频（如 __SYSTEM_CLOCK_168M_PLL_25M_HXTAL）

STM32 vs GD32 常见差异：
- 时钟单元命名：STM32 的 RCC vs GD32 的 RCU
- Flash 控制：STM32 的 FLASH->ACR vs GD32 的 FMC/EFMC 等寄存器布局差异
- 目标频率方案：CubeMX 生成的 STM32 system 文件按 HAL 统一风格计算；GD32 官方 system 文件常通过宏开关直选目标频率
- HSE/HXTAL 名称与默认值不同


### 1.2 外设库函数（Standard Peripheral Library）

- **作用**: 封装底层寄存器操作，提供高级API
- **文件结构**:
  - `Include/`: 头文件（如`gd32f4xx_gpio.h`, `gd32f4xx_usart.h`）
  - `Source/`: 实现文件（如`gd32f4xx_gpio.c`, `gd32f4xx_usart.c`）

### 1.3 启动文件（Startupxx.s）

- **文件**: startup_gd32f407_427.S

**主要作用简介**:
  - 定义中断向量表
  - 初始化栈指针
  - 复制数据段从Flash到RAM
  - 清零BSS段
  - 调用`SystemInit()`和`main()`

具体分析：
- 设置栈指针（如果不是由向量表设置，也会在此确认）
- 复制 .data：从 Flash 的 _sidata 到 RAM 的 [_sdata, _edata)
- 清零 .bss：[_sbss, _ebss)
- 调用 SystemInit 配置系统时钟、Flash 等
- 调用 __libc_init_array（C++ 全局构造/静态初始化）
- 跳转 main
- 定义中断向量表（一个以函数地址构成的表），并对每个 ISR 提供 weak 别名到 Default_Handler，便于用户覆写

与 ld 的耦合：
- 完全依赖 ld 导出的段符号做内存搬运
- 向量表符号名必须与 ld 中 .vectors/.isr_vector 入口一致，才能被放对位置
- 需要与内核一致的异常顺序（架构规定）以及与芯片一致的外设中断顺序（芯片定义），否则中断号错位

STM32 vs GD32 常见差异：
- 向量表里外设中断的“顺序与名称”可能不同（如 TIM/USART/DMA 编号与路由）
- 默认调用的系统初始化函数名相同（SystemInit），但实现细节不同
- 某些启动文件会在 Reset_Handler 之前就设置 VTOR 或 FPU

### 1.4 链接器脚本（Linker Script）

- **文件**: gd32f4xx_flash.ld

**主要作用简介**:
  - 定义内存布局（Flash、RAM、TCM等）
  - 指定代码段、数据段的存储位置
  - 设置入口点（Reset_Handler）

具体分析：
- 定义存储器映射 MEMORY：例如
  - FLASH ORIGIN=0x08000000, LENGTH=…
  - RAM/TCMRAM ORIGIN=0x20000000/0x10000000
- 分配段 SECTIONS：
  - .vectors/.isr_vector：中断向量表放在 Flash 开头
  - .text/.rodata 放 Flash；.data 放 RAM（镜像在 Flash），.bss 放 RAM
  - 导出符号：_sidata（data 源地址）、_sdata/_edata（data 目的范围）、_sbss/_ebss（bss 范围）、_estack（栈顶）、__gVectors 或 __isr_vector（向量表符号）
- 运行时/异常展开段：.ARM.exidx/.ARM.extab（可选）
- 与文件配合点：startup 用它提供的符号地址；system 可能依赖外设地址和时钟频率常量；it 与 ld 无直接耦合，但 ISR 地址最终收敛进 .vectors。

常见差异与注意（STM32 vs GD32）：
- Flash/RAM/TCM 大小与基址可能不同（GD32F470 有 TCMRAM：0x10000000）
- .vectors 段名可能不同（STM32 工程常叫 .isr_vector；GD32 示例里使用 __gVectors 并在 .vectors 里引用）
- 若向量表需搬到 SRAM，ld 里需给 SRAM 里的表预留空间并暴露符号，startup 里用 SCB->VTOR 重定位。


## 2. make + arm-none-eabi-gcc 编译流程

 **第1步：预处理（Preprocessing）**
```bash
arm-none-eabi-gcc -E -mcpu=cortex-m4 -mthumb -I./inc -I./Firmware/CMSIS/Include -I./Firmware/GD32F4xx_standard_peripheral/Include main.c -o main.i
```
- **作用**: 处理`#include`、`#define`等预处理指令
- **输入**: `.c`源文件
- **输出**: `.i`预处理文件

 **第2步：编译（Compilation）**
```bash
arm-none-eabi-gcc -S -mcpu=cortex-m4 -mthumb -mfloat-abi=soft main.i -o main.s
```
- **作用**: 将C代码编译为ARM汇编代码
- **输入**: `.i`预处理文件
- **输出**: `.s`汇编文件

 **第3步：汇编（Assembly）**
```bash
arm-none-eabi-as -mcpu=cortex-m4 -mthumb main.s -o main.o
arm-none-eabi-as -mcpu=cortex-m4 -mthumb startup_gd32f407_427.S -o startup.o
```
- **作用**: 将汇编代码转换为机器码
- **输入**: `.s`汇编文件和`.S`启动文件
- **输出**: `.o`目标文件

 **第4步：链接（Linking）**
```bash
arm-none-eabi-ld -T gd32f4xx_flash.ld main.o startup.o gpio.o usart.o ... -o firmware.elf
```
- **作用**: 
  - 合并所有目标文件
  - 根据链接器脚本分配内存地址
  - 解析符号引用
- **输入**: 所有`.o`文件 + 链接器脚本
- **输出**: `.elf`可执行文件

 **第5步：生成烧录文件**
```bash
arm-none-eabi-objcopy -O binary firmware.elf firmware.bin
arm-none-eabi-objcopy -O ihex firmware.elf firmware.hex
```
- **作用**: 转换为烧录器可识别的格式
- **输出**: `.bin`或`.hex`文件

- 典型Makefile结构

```makefile
# 工具链定义
CC = arm-none-eabi-gcc
AS = arm-none-eabi-as
LD = arm-none-eabi-ld
OBJCOPY = arm-none-eabi-objcopy

# 编译选项
CFLAGS = -mcpu=cortex-m4 -mthumb -mfloat-abi=soft -O2 -g
ASFLAGS = -mcpu=cortex-m4 -mthumb
LDFLAGS = -T gd32f4xx_flash.ld

# 头文件路径
INCLUDES = -I./inc \
           -I./Firmware/CMSIS/Include \
           -I./Firmware/GD32F4xx_standard_peripheral/Include

# 源文件列表
SOURCES = src/main.c \
          src/systick.c \
          Firmware/GD32F4xx_standard_peripheral/Source/gd32f4xx_gpio.c \
          Firmware/GD32F4xx_standard_peripheral/Source/gd32f4xx_rcu.c

STARTUP = gcc_startup/startup_gd32f407_427.S

# 编译规则
all: firmware.bin

firmware.bin: firmware.elf
	$(OBJCOPY) -O binary $< $@

firmware.elf: $(SOURCES:.c=.o) $(STARTUP:.S=.o)
	$(LD) $(LDFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

%.o: %.S
	$(AS) $(ASFLAGS) $< -o $@
```

## 3. 编译过程中各文件作用

1. **CMSIS文件**: 提供标准化的硬件抽象接口
2. **外设库**: 简化外设操作，提高开发效率
3. **启动文件**: 确保MCU正确启动和初始化
4. **链接器脚本**: 决定程序在内存中的布局
5. **主程序**: 实现具体的应用逻辑

这个编译流程确保了从高级C代码到最终可烧录的二进制文件的完整转换过程，每个步骤都有其特定的作用和输出。

# 二: 连接/调用关系


## 1. 连接关系

- ld 决定“放哪儿”和“段边界符号叫什么”
- startup 依赖 ld 的符号完成数据搬运/清零，并输出向量表
- system 由 startup 调用，完成时钟/Flash 配置并更新 SystemCoreClock
- it 提供与向量表同名的 ISR，覆盖 weak 默认处理

一处不匹配就可能导致：
- 向量表错位或未放在正确地址：上电即 HardFault
- 段边界符号不一致：.data 未拷贝或 .bss 未清零，运行异常
- 时钟/Flash 等待周期设置不当：随机 HardFault/BusFault
- ISR 命名或顺序不一致：中断跑飞或死循环

## 2. 调用关系

这些文件的调用关系不清楚，比如core_cm4.h: Cortex-M4内核定义，我没有看到有文件include core_cm4.h，它在哪里被调用呢？包括core_cm4.h、gd32f4xx.h、system_gd32f4xx.h等的相互调用关系？

```
main.c → gd32f4xx.h → core_cm4.h + system_gd32f4xx.h
                   ↑
所有外设库源文件和中断处理文件都会包含 gd32f4xx.h
```

**具体调用路径**：
1. **应用层文件**（如main.c, systick.c等）：
   ```c
   #include "gd32f4xx.h"  // 主头文件
   ```

2. **gd32f4xx.h内部包含**：
   ```c
   #include "core_cm4.h"        // Cortex-M4核心定义
   #include "system_gd32f4xx.h" // 系统配置
   #include <stdint.h>          // 标准类型定义
   ```

3. **所有外设库文件**（如gd32f4xx_gpio.c等）都包含对应的头文件：
   ```c
   #include "gd32f4xx_gpio.h"
   ```
   而这些头文件最终都会包含gd32f4xx.h

4. **中断处理文件**gd32f4xx_it.c：
   ```c
   #include "gd32f4xx_it.h"
   ```
   gd32f4xx_it.h内部包含gd32f4xx.h


## 3. 是否重复定义问题？


### 3.1 中断向量的定义

gd32f4xx.h定义（寄存器、中断向量等），但是startup_gd32f450_470.S定义中断向量表，这不重复定义了吗？这两个文件的关系和在这个过程中的调用顺序是什么？

**这两个文件并不重复定义，而是分工明确**：

 **gd32f4xx.h中的中断定义**：
- 定义**中断号枚举**（`IRQn_Type`）
- 为编译器和C代码提供中断号常量
- 用于NVIC配置和中断优先级设置

 **startup_gd32f407_427.S中的中断向量表**：
- 定义**实际的中断向量表**（`__gVectors`）
- 每个中断号对应一个具体的函数地址
- 存储在Flash的固定位置（0x08000000）

 **调用顺序**：
1. **编译时**：gd32f4xx.h提供中断号定义给C代码使用
2. **链接时**：启动文件的向量表被放置在Flash起始位置
3. **运行时**：CPU根据向量表跳转到对应的中断处理函数

```assembly
/* 启动文件中的向量表 */
__gVectors:
    .word _sp                    /* 栈顶指针 */
    .word Reset_Handler          /* 复位中断 */
    .word NMI_Handler           /* NMI中断 */
    .word HardFault_Handler     /* 硬件错误中断 */
    /* ... 更多中断向量 ... */
```

- 链接脚本定义内存布局和符号
- 启动文件使用这些符号进行内存初始化
- 两者在链接阶段结合，运行时协同工作

### 3.2 内存布局的定义

- （2）startup_gd32f450_470.S复制数据段从Flash到RAM，包括清零BSS段，调用SystemInit()和main()，但是gd32f4xx_flash.ld文件定义内存布局（Flash、RAM、TCM等），前者会调用后者拿到内存布局定义吗？

**启动文件不会"调用"链接脚本，而是在编译链接时协同工作**：

 **工作流程**：
1. **编译时**：
   - 启动文件中使用符号`_sidata`, `_sdata`, `_edata`, `_sbss`, `_ebss`
   - 这些符号此时是**未定义**的

2. **链接时**：
   - 链接器根据gd32f4xx_flash.ld脚本：
     ```ld
     _sidata = LOADADDR(.data);    /* Flash中数据段起始地址 */
     .data : {
         _sdata = .;               /* RAM中数据段起始地址 */
         *(.data)
         _edata = .;               /* RAM中数据段结束地址 */
     } > RAM AT> FLASH

     .bss : {
         _sbss = .;                /* BSS段起始地址 */
         *(.bss)
         _ebss = .;                /* BSS段结束地址 */
     } > RAM
     ```

3. **运行时**：
   - CPU执行`Reset_Handler`
   - 使用链接器定义的符号进行数据初始化：
     ```assembly
     Reset_Handler:
         /* 复制.data段从Flash到RAM */
         ldr r3, =_sidata    /* Flash中的数据源地址 */
         ldr r0, =_sdata     /* RAM中的数据目标地址 */
         ldr r3, =_edata     /* 数据段结束地址 */
         
         /* 清零.bss段 */
         ldr r2, =_sbss      /* BSS段起始地址 */
         ldr r3, =_ebss      /* BSS段结束地址 */
     ```

# 三: bootloader过程
烧录到启动的过程是怎样的（每个步骤与哪些文件相关）；


## 第1阶段：烧录过程

 **1.1 固件生成**
```bash
# 编译生成ELF文件
arm-none-eabi-gcc ... -T gd32f4xx_flash.ld ... -o firmware.elf

# 转换为烧录格式
arm-none-eabi-objcopy -O binary firmware.elf firmware.bin
arm-none-eabi-objcopy -O ihex firmware.elf firmware.hex
```
**相关文件**：
- gd32f4xx_flash.ld - 定义Flash内存布局
- startup_gd32f407_427.S - 向量表和启动代码
- 所有应用程序文件

 **1.2 烧录到Flash**
```bash
# 使用OpenOCD烧录
openocd -f openocd_gdlink.cfg -c "program firmware.bin 0x08000000 verify reset exit"
```

**Flash内存布局**：
```
0x08000000: [向量表] - 1KB
            - 栈顶指针 (4字节)
            - Reset_Handler地址 (4字节)
            - 其他中断向量 (每个4字节)
0x08000400: [程序代码] - 应用程序
0x080xxxxx: [常量数据] - const变量
```

## 第2阶段：硬件复位启动

### 2.1 硬件复位

上电/复位后，检查BOOT引脚，根据高低电平状态决定从哪里找启动代码（比如是哪个flash，flash的哪个地址开始之类的）。一般是BOOT0和BOOT1的组合，具体见芯片参考手册。


- Cortex‑M4 从地址 0x00000000 读取两个字：
  - [0x00000000] 初始 MSP 值（栈顶）
  - [0x00000004] Reset_Handler 的入口地址（PC）一般指针指向`0x08000000`
- 这两项来自“中断向量表”的前两项。向量表一般放在 Flash “如STM32F429XX_FLASH.ld” 并通过厂商的映射机制出现在 0x00000000。

- 从向量表读取栈顶指针和Reset_Handler地址

### 2.2 CPU初始化

```assembly
/* 硬件自动执行 */
SP = *0x08000000          // 设置栈指针
PC = *0x08000004          // 跳转到Reset_Handler
```

## 第3阶段：软件启动过程

### 3.1 Reset_Handler执行
 
**文件**：startup_gd32f407_427.S

- 初始化数据段/清零 bss 段（依赖 ld 文件里导出的段边界符号）
- 可选：设置堆/栈、FPU 开关、VTOR 重定位向量表到 SRAM
- 调用 SystemInit 配置时钟/Flash 等硬件
- 运行 C 运行时构造器（__libc_init_array）
- 跳转到 main

```assembly
Reset_Handler:
  /* 1. 复制.data段从Flash到RAM */
  movs r1, #0
  b DataInit
CopyData:
  ldr r3, =_sidata    // Flash中初始化数据
  ldr r3, [r3, r1]
  str r3, [r0, r1]    // 复制到RAM
  adds r1, r1, #4
DataInit:
  ldr r0, =_sdata     // RAM数据段起始
  ldr r3, =_edata     // RAM数据段结束
  adds r2, r0, r1
  cmp r2, r3
  bcc CopyData

  /* 2. 清零.bss段 */
  ldr r2, =_sbss
  b Zerobss
FillZerobss:
  movs r3, #0
  str r3, [r2], #4
Zerobss:
  ldr r3, = _ebss
  cmp r2, r3
  bcc FillZerobss

  /* 3. 调用SystemInit */
  bl  SystemInit

  /* 4. 调用C库构造函数 */
  bl __libc_init_array

  /* 5. 跳转到main函数 */
  bl main
```

### 3.2 SystemInit执行

**文件**：system_gd32f4xx.c
```c
void SystemInit(void)
{
    /* 1. 配置FPU */
#if (__FPU_PRESENT == 1) && (__FPU_USED == 1)
    SCB->CPACR |= ((3UL << 10*2)|(3UL << 11*2));
#endif

    /* 2. 复位RCU时钟配置 */
    RCU_CTL |= RCU_CTL_IRC16MEN;
    
    /* 3. 配置系统时钟 */
    system_clock_config();
}
```

### 3.3 主程序执行

**文件**：main.c
```c
int main(void)
{
    /* 用户应用程序 */
    return 0;
}
```

### 3.4 运行期中断


# 四: 自定义bootloader

比如我自己想自定义一个启动过程，写一个 bootloader 应该如何操作？bootloader这个过程又是在哪个文件定义的？

## Bootloader架构设计

```
Flash布局：
0x08000000: [Bootloader] - 16KB
0x08004000: [Application] - 剩余空间
0x080XXXXX: [配置区域] - 4KB (存储升级标志等)
```

| 阶段                | 相关文件                   | 作用                            |
| ----------------- | ---------------------- | ----------------------------- |
| **硬件复位**          | 无                      | CPU自动从0x08000000读取向量表         |
| **Bootloader启动**  | bootloader_startup.S   | 定义Bootloader向量表和Reset_Handler |
| **Bootloader初始化** | bootloader_main.c      | 系统初始化、检查升级标志                  |
| **应用程序检查**        | bootloader_main.c      | 验证应用程序有效性                     |
| **跳转应用程序**        | bootloader_main.c      | 重新配置向量表，跳转到应用程序               |
| **应用程序启动**        | startup_gd32f407_427.S | 应用程序的Reset_Handler            |

## Bootloader关键功能

1. **固件验证**：检查应用程序完整性
2. **固件升级**：通过UART/USB等接口接收新固件
3. **安全跳转**：正确设置栈指针和向量表后跳转
4. **错误恢复**：应用程序损坏时提供恢复机制

## 使用示例

```bash
# 编译Bootloader和应用程序
make -f Makefile_bootloader all

# 烧录完整固件
make -f Makefile_bootloader flash

# 仅更新应用程序（通过Bootloader）
make -f Makefile_bootloader flash-application
```

这样的设计实现了：
- **固件保护**：Bootloader独立存储，不会被应用程序破坏
-  **在线升级**：支持远程固件更新
-  **快速启动**：正常情况下快速跳转到应用程序
-  **故障恢复**：应用程序损坏时可通过Bootloader恢复


# 五: 程序移植简要说明


- 链接脚本：
  - Flash/RAM/TCM 容量与基址是否匹配目标芯片
  - .vectors 段名与 startup 中的向量表符号一致（__gVectors 或 .isr_vector）
- 启动文件：
  - 向量表“顺序与名称”符合 GD32 数据手册
  - Reset_Handler 使用的段边界符号与 ld 一致
- system 文件：
  - 使用 GD32 的时钟/Flash 控制寄存器与宏（RCU/FMC vs RCC/FLASH）
  - HXTAL/IRC16M 值设置正确；SystemCoreClock 正确
- it 文件：
  - ISR 名称与 GD32 启动向量表一致，或提供别名映射
  - NVIC IRQn 使用 GD32 的枚举


- 查看向量表位置与内容：
  - arm-none-eabi-objdump -h your.elf | grep -E "vectors|isr"
  - arm-none-eabi-objdump -D your.elf | sed -n '1,120p'  # 检查起始几项是否为 _estack/Reset_Handler
- 确认符号是否导出：
  - arm-none-eabi-nm your.elf | grep -E "_sidata|_sdata|_edata|_sbss|_ebss|_estack|__gVectors|g_pfnVectors"
- 运行期核对时钟：
  - 在 main 里调用 SystemCoreClockUpdate 后打印/断点检查 SystemCoreClock