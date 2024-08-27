
# 开发环境
## Reference
- [STM32开发环境搭建(ARM-GCC)](https://microdynamics.github.io/1.%20Breeze%20Mini四轴飞行器/2.2%20STM32开发环境搭建(ARM-GCC)/)
- [windows开源STM32开发环境](https://blog.csdn.net/zhangfan2256/article/details/132196426)
- [Windows 下构建 STM32 开发环境](https://wangyuyang.me/posts/windows下构建stm32开发环境/)
- [VsCode+OpenOCD 开发stm32系列](https://blog.csdn.net/pyt1234567890/article/details/122522700)
- [在Mac OS X中搭建STM32开发环境](https://www.cnblogs.com/humaoxiao/p/3576732.html "发布于 2014-03-02 13:52")
- [STM32CubeMX](https://www.stmcu.com.cn/ecosystem/Cube/STM32cubemx)
- [ STM32 下载器调试器——DAPLink](https://sspai.com/post/88682)
- [VSCode STM32_development](https://stm32world.com/wiki/STM32_development_and_debugging_using_VSCode#google_vignette)
## 开发环境配置
不使用 IDE，而是通过命令行工具和其他独立工具进行 STM32开发，优点就是开源免费且无需担心法律风险，官网或者github下载无需担心安装包风险，有利于深入了解开发工具，缺点就是更费时。
整个开发过程可以按照以下步骤进行：安装工具、开发、编译、烧录和调试。在这个流程中，完全依赖命令行工具和文本编辑器进行开发。STM32CubeMX 用于生成初始化代码，vscode用来写代码，armGNU 工具链用于编译代码，OpenOCD 用于烧录和调试。
当然，如果使用STM32CubeIDE，这些工具都无需配置，下文讲一讲STM32Cube包的关系。
### STM32Cube包的关系
本来是vscode-stm32插件，结果stm插件有问题，多了很多依赖，就研究了一下这几个依赖的关系---[STM32CubeCLT](https://www.st.com/en/development-tools/stm32cubeclt.html)、[STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html)和[STM32CubeIDE](https://www.st.com.cn/zh/development-tools/stm32cubeide.html)的关系。BTW，也没必要整太多插件，手动写写配置文件比较好，能熟悉一下每个工具。
#### STM32CubeMX
[STM32CubeMX](https://www.st.com.cn/zh/development-tools/stm32cubemx.html)生成适用于stm32具体机型的初始化c代码（还有一些初始化硬件如时钟、端口等功能），它的目的是让用其他平台的开发者快速形成可用的stm32的C语言代码，所以它没有代码编辑器、交叉编译器、下载器、调试器等很多工具。

- 直观的STM32微控制器和微处理器选择 
- 丰富易用的图形用户界面，允许配置： 
    - 支持自动冲突解决的引脚分配 
    - 支持面向Arm® Cortex®-M内核带参数约束动态验证的外设和中间件功能模式 
    - 支持动态验证时钟树配置 
    - 带功耗结果估算的功耗序列 
- 生成与面向Arm® Cortex®-M内核的IAR Embedded Workbench®、MDK-ARM和STM32CubeIDE（GCC编译器）兼容的初始化C代码 
- 生成面向Arm® Cortex®-A内核（STM32微处理器）的部分Linux®设备树 
- 借助STM32PackCreator开发增强型STM32Cube扩展包 
- 将STM32Cube扩展包集成到项目中 
- 作为可在Windows®、Linux®和macOS®（macOS®是苹果公司在美国和其他国家与地区的商标）操作系统和64位Java运行环境上运行的独立软件提供 and other countries.) operating systems and 64-bit Java Runtime environment
#### STM32CubeCLT
集成了交叉编译器、下载器、调试器等很多工具，因为是命令行工具，所以需要加入环境变量，不过若使用命令行开发，交叉编译器、下载器、调试器都无需下载stm的，而是下载开源通用的，这样有利于开发其他平台。
- Distribution of command-line tools and system view descriptors (SVD) extracted from STM32CubeIDE 
- STM32Cube MCU Packages support for STM32 microcontrollers (MCU) at the following development steps: 
    - Compile and link 
    - Target board programming 
    - Application run 
    - Application debugging 
- The STM32CubeCLT toolset includes: 
    - GNU C/C++ for Arm® toolchain executables such as arm-none-abi-gcc (compiler), arm-none-abi-nm (symbol viewer), and many more 
    - GDB debugger client and server 
    - STM32CubeProgrammer (STM32CubeProg) utility 
    - System view descriptor files (.SVD) for the entire STM32 MCU portfolio 
    - Map file associating STM32 MCUs and MCU development boards to the appropriate SVD

#### STM32CubeIDE
[STM32CubeIDE](https://www.st.com.cn/zh/development-tools/stm32cubeide.html)是一个“集大成”软件，其集成了STM32CubeMX的功能，同时也集成了STM32CubeCLT的功能，还继承了代码编辑器(代码高亮跳转等功能)的功能，也就是类似apple平台开发下的Xcode，或者windows下的Visual Studio。

- 通过STM32CubeMX来集成服务：STM32微控制器、微处理器、开发平台和示例项目选择引脚排列、时钟、外设和中间件配置项目创建和初始化代码生成具有增强型STM32Cube扩展包的软件和中间件
- 基于Eclipse®/CDT™，支持Eclipse®插件、GNU C/C++ for Arm®工具链和GDB调试器 
- STM32MP1 系列：支持OpenSTLinux项目：Linux支持Linux
- 其他高级调试功能包括：CPU内核、外设寄存器和内存视图实时变量查看视图系统分析与实时跟踪(SWV)CPU故障分析工具支持RTOS感知调试，包括Azure
- 支持ST-LINK（意法半导体）和J-Link (SEGGER)调试探头 
- 从Atollic® TrueSTUDIO®和AC6 System Workbench for STM32 (SW4STM32)导入项目
### 1. 安装必要的工具
首先，需要安装以下工具：（别忘了检查是否加入环境变量）
- [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html)：用于生成初始化代码。
- [GNU Arm Embedded Toolchain Downloads](https://developer.arm.com/downloads/-/gnu-rm)：用于交叉编译编译代码。
- [OpenOCD](https://openocd.org/pages/getting-openocd.html)：用于烧录和调试。或者[pyocd](https://pyocd.io/docs/)
- [STlink驱动](https://www.st.com.cn/zh/development-tools/stsw-link009.html)：用于烧录。或者[cmsis-DAP-v2](https://arm-software.github.io/CMSIS_5/DAP/html/dap_install.html)（不需要驱动）
- **GCC & Make & git**：用于管理构建过程（可选，如果使用 `Makefile`）。不同操作系统的开发机器有所不同，windows安装msys2安装mingw64，mac就是xcode，linux则是build-essential。
- vscode或者sublime用于写代码：更推荐vscode用来写一些有一定体量的工程化代码，sublime更轻量功能也更少一些。

### gcc-arm-embedded 和 arm-none-eabi-gcc 区别
`gcc-arm-embedded` 和 `arm-none-eabi-gcc` 都是用于编译ARM架构嵌入式系统代码的编译器工具链，它们之间的主要区别如下：

1. **维护者和发布渠道**:
   - `gcc-arm-embedded`: 由Arm（原ARM公司）官方发布和维护，通常会在[Arm Developer网站](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm)上发布。它通常被视为官方推荐的工具链版本。
   - `arm-none-eabi-gcc`: 这是一个通用的名称，通常指的是GNU Arm Embedded Toolchain。它可以通过多种渠道获取，比如通过Linux的包管理器（如APT）安装，也可以通过其他工具链发行版本获取，如通过ARM的官网下载或者直接通过GNU的官方工具链仓库获取。

2. **发行版本和更新频率**:
   - `gcc-arm-embedded`: Arm官方发布的版本通常经过特定的测试，并且针对特定的硬件架构进行优化和稳定性验证。更新频率可能与 `arm-none-eabi-gcc` 略有不同，通常会提供一些针对性优化。
   - `arm-none-eabi-gcc`: 这个版本通常跟随GCC的官方发布节奏更新，可能会更频繁地获得更新和新特性，但也可能包含一些实验性功能。

3. **安装方式**:
   - `gcc-arm-embedded`: 通常通过下载预构建的二进制文件安装，或者通过一些IDE（如STM32CubeIDE）集成的工具链安装。
   - `arm-none-eabi-gcc`: 可以通过Linux发行版的包管理器直接安装（如通过 `apt-get install gcc-arm-none-eabi`），也可以通过其他方式获取。

4. **支持的功能和优化**:
   - `gcc-arm-embedded`: 可能包含一些ARM官方特有的优化和补丁，专门用于特定的ARM芯片。
   - `arm-none-eabi-gcc`: 作为GCC的一部分，提供了更广泛的GCC特性，适用于更广泛的使用场景，但某些特定优化可能不如`gcc-arm-embedded`专注。

总体来说，`gcc-arm-embedded` 更加偏向于官方提供的ARM嵌入式开发工具链，经过ARM官方的优化和测试。`arm-none-eabi-gcc` 则是一个通用的工具链版本，可能包含更多GCC的特性和最新的更新，但优化上未必专注于某些ARM芯片。

对于大多数嵌入式开发项目，尤其是针对ARM Cortex-M系列开发时，选择 `gcc-arm-embedded` 会更为稳妥，因为这是经过官方认证的工具链。
#### vscode config
可以设置个`.vscode`文件夹，然后设置上`settings.json`、`c_cpp_properties.json`、`tasks.json`和`launch.json`。不用整这些（`c_cpp_properties.json`还是要的，不然vscode找不到函数/变量的引用），直接打开vscode中的terminal然后make就行（make和交叉编译的exe文件夹都要加入环境变量）。 
```json
// tasks.json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "type": "shell",
            "command": "make",
            "args": [
            ],
            "group": "build"
        },
        {
            "label": "download",
            "type": "shell",
            "command": "openocd",
            "args": [
                "-f",
                "cmsis-dap.cfg",
                "-f",
                "stm32h7x.cfg",
                "-c",
                "program build/stm32h7_demo.elf verify reset exit"
            ],
            "group": "build"
        }
    ]
}

// c_cpp_properties.json

```
### 2. 使用 STM32CubeMX 配置项目
1. **打开 STM32CubeMX - file**。
2. **创建新项目**：
   - 选择微控制器型号（如 STM32L010）。
   - 配置外设、时钟、引脚和中断等设置。
3. **生成代码**：
   - 选择生成的项目类型为 Makefile 项目（如果使用 Makefile），或直接生成 C 代码。
   - STM32CubeMX 会生成初始化代码，包括启动文件和 HAL 库。

### 3. 编写和配置代码
1. **编辑生成的代码**：
   - 使用文本编辑器（如 VSCode、Sublime Text 等）编辑代码。
   - 添加应用逻辑代码，修改或扩展 STM32CubeMX 生成的初始化代码。

2. **版本管理**：git
这个就不介绍了，不用操作系统的开发机器有所不同，去官网看doc怎么用就ok

3. **创建 Makefile**：
   - 如果 STM32CubeMX 没有生成 Makefile，需要自己编写一个 Makefile。
   - Makefile 应该指定编译器路径、编译选项、链接选项和输出文件路径。

### 4. 编译代码
   - 打开命令行，导航到项目目录。
   - 使用 Makefile 进行编译：`make`
   - 如果没有使用 Makefile，可以手动使用 `arm-none-eabi-gcc` 命令进行编译和链接。例如：
     ```bash
     arm-none-eabi-gcc -o main.o -c main.c -mcpu=cortex-m0 -mthumb
     arm-none-eabi-gcc -o main.elf main.o -TSTM32L010.ld -mcpu=cortex-m0 -mthumb -nostartfiles
     arm-none-eabi-objcopy -O binary main.elf main.bin
     ```
   - 编译得到一个二进制文件（如 `.elf` 或 `.bin`）。
#### makefile添加新的代码文件
在makefile里面修改两处地方：`C_SOURCES`和`C_INCLUDES`。
在`C_SOURCES`里面添加你`.c`文件的相对路径，在`C_INCLUDES`中添加`.h`文件的所在目录的相对路径（需要加`-I`前缀）。
 

### 5. 烧录代码
1. **连接开发板**：
   - 通过 USB 将 ST-LINK 或 CMSIS-DAP 适配器连接到开发板和电脑。
   - 安装[ST-link驱动](https://www.st.com.cn/zh/development-tools/stsw-link009.html)。
   
2. **配置 OpenOCD**：
   - 确保 OpenOCD 已安装并配置好。还需要一个 OpenOCD 配置文件（`*.cfg`），它指定目标芯片和调试适配器。
   - copy `your_openocd_dir/openocd/scripts/interface/stlink.cfg`and `your_openocd_dir/openocd/scripts/target/stm32l0.cfg` to your project folder.
   - 使用以下命令启动 OpenOCD：
     ```sh
     openocd -f stlink.cfg -f stm32l0.cfg -c init -c halt -c "flash write_image erase build/yourfile.bin 0x08000000" -c reset -c shutdown
     ```
或者，写到makefile里，然后用make download命令运行。
```bash
#######################################
# make download
#######################################
OPENOCD_INTERFACE = stlink-v2-1.cfg
OPENOCD_TARGET = stm32l4x.cfg
OPENOCD_FLASH_START = 0x08000000

download:
 openocd -f $(OPENOCD_INTERFACE) -f $(OPENOCD_TARGET) -c init -c halt -c "flash write_image erase $(BUILD_DIR)/$(TARGET).bin $(OPENOCD_FLASH_START)" -c reset -c shutdown
```

3. **烧录代码**：
   - 在命令行中使用以下命令进行烧录：
     ```sh
     openocd -f interface/stlink.cfg -f target/stm32l0.cfg -c "program main.elf verify reset exit"
     ```
   - 这将把 `main.elf` 文件烧录到 STM32 微控制器中，并复位芯片。

### 6. 调试
- [opocd+GDB调试stm32](http://116.205.174.47/2023/04/04/linux/arm/stm32-openocd-gdb/095427/)

![GDB调试流程](stm32-develop.assets/GDB调试流程.png)
1. **启动调试会话**：
   - 使用 GDB（GNU 调试器）来连接 OpenOCD 进行调试。首先启动 OpenOCD：
     ```sh
     openocd -f interface/stlink.cfg -f target/stm32l0.cfg
     ```
   
2. **使用 GDB 连接**：
   - 在另一个终端窗口中，启动 GDB 并连接到 OpenOCD：
     ```sh
     arm-none-eabi-gdb main.elf
     target remote localhost:3333
     ```
   - 可以在 GDB 中设置断点、单步执行代码、检查寄存器和内存等。

# HAL库
- [野火STM32 HAL库开发](https://doc.embedfire.com/mcu/stm32/f103/hal_general/zh/latest/index.html)（有对应的PDF在apple books）但是最好先看手册（官网有中文版比如M0的PDF在apple books）查资料，这个野火的教程不适合入门，一个是对基本原理不讲或讲的太杂太细，二是有大量的宏定义，反而让初学者缕不清HAL库的函数调用。

![stm32软件架构](stm32-develop.assets/stm32软件架构.png)
## C 语言对寄存器的封装
这部分就是浅尝辄止的了解一下HAL库的工作，就不深入了解重复造轮子了。（有时间还是要造一遍）
### 宏定义封装地址
这当然不是最终的封装，因为还是有大量位操作。
```c
// 外设基地址
define PERIPH_BASE ((unsigned int)0x40000000)

// 总线基地址
define APB1PERIPH_BASE PERIPH_BASE
define APB2PERIPH_BASE (PERIPH_BASE + 0x00010000)
define AHBPERIPH_BASE (PERIPH_BASE + 0x00020000)

// GPIO 外设基地址
define GPIOA_BASE (APB2PERIPH_BASE + 0x0800)
define GPIOB_BASE (APB2PERIPH_BASE + 0x0C00)
define GPIOC_BASE (APB2PERIPH_BASE + 0x1000)
define GPIOD_BASE (APB2PERIPH_BASE + 0x1400)
define GPIOE_BASE (APB2PERIPH_BASE + 0x1800)
define GPIOF_BASE (APB2PERIPH_BASE + 0x1C00)
define GPIOG_BASE (APB2PERIPH_BASE + 0x2000)

// 寄存器基地址，以GPIOB 为例
define GPIOB_CRL (GPIOB_BASE+0x00)

/* 控制GPIOB 引脚0 输出低电平(BSRR 寄存器的BR0 置1) */
*(unsigned int *)GPIOB_BSRR = (0x01<<(16+0));

/* 控制GPIOB 引脚0 输出高电平(BSRR 寄存器的BS0 置1) */
*(unsigned int *)GPIOB_BSRR = 0x01<<0;
unsigned int temp;

/* 读取GPIOB 端口所有引脚的电平(读IDR 寄存器) */
temp = *(unsigned int *)GPIOB_IDR;
```

### 结构体封装寄存器组
```c
typedef unsigned int uint16_t; /* 无符号16 位变量*/
typedef unsigned short int uint32_t; /* 无符号32 位变量*/

/* GPIO 寄存器列表“封装”为一个结构体 */
typedef struct {
uint32_t CRL; /*GPIO 端口配置低寄存器 地址偏移: 0x00 */
uint32_t CRH; /*GPIO 端口配置高寄存器 地址偏移: 0x04 */
uint32_t IDR; /*GPIO 数据输入寄存器 地址偏移: 0x08 */
uint32_t ODR; /*GPIO 数据输出寄存器 地址偏移: 0x0C */
uint32_t BSRR; /*GPIO 位设置/清除寄存器 地址偏移: 0x10 */
uint32_t BRR; /*GPIO 端口位清除寄存器 地址偏移: 0x14 */
uint16_t LCKR; /*GPIO 端口配置锁定寄存器 地址偏移: 0x18 */
} GPIO_TypeDef;

GPIO_TypeDef * GPIOx; //定义一个GPIO_TypeDef 型结构体指针GPIOx
GPIOx = GPIOB_BASE; //把指针地址设置为宏GPIOB_BASE 地址
GPIOx->IDR = 0xFFFF;
GPIOx->ODR = 0xFFFF;

uint32_t temp;
temp = GPIOx->IDR; //读取GPIOB_IDR 寄存器的值到变量temp 中
```
### 封装寄存器的位操作方法
。。。

## 时钟
- [# STM32CubeMX使用 之“吃透RCC”](https://www.bilibili.com/video/BV1Qe411W7rv/)
内部时钟，外部高速/低速时钟的设置。设置外部时钟首先需要开发版或者电路板按照芯片datasheet正确连接了外部晶振。然后在CubeMX中(Pinout&config---sys中)开启，然后在Clock config页面中选择设置等，具体看视频链接。

## 中断
- [STM32 CubeMX外部中断EXTI](https://www.bilibili.com/video/BV12Q4y1K74V/)
上述链接视频讲解得不错，比如讲到了函数`void HAL_GPIO_EXIT_Callback(uint16_t GPIO_Pin)`是HAL库的一个弱函数(__weak)，我们是重写。还有在STM32CubeMX中如何设置实现GPIO的外部中断。

## 定时器
定时器一定要与中断配合才有意义。stm32有几类不同的定时器，

### 基本定时器操作
#### 1. CubeMX
1.1 tim2(其中一个通用定时器)，Clock Source选择internal clock 
1.2 Counter Settings 
#### 2. 代码
![](stm32-develop.assets/stm32_HAL_定时器开关函数.jpg)


### 定时器问题
#### 定时器中断无法使用HAL_Delay
- [](https://blog.csdn.net/m0_57147943/article/details/123518122)

## GPIO

### IO的硬件原理
[STM32CubeMX使用-吃透IO口](https://b23.tv/hyxZ4tR)
上述链接的视频比较简单清楚的讲解了io的硬件原理，可以简单的理解上下拉电阻的优缺点（优点抗干扰能力强，缺点被上拉/下拉电阻分压导致高低电平分压而），如何复用IN/OUT、推挽与开漏的区别等问题，结构图如下：
![](stm32-develop.assets/stm32IO硬件结构示意图.png)

### 共阳极控制
- [共阳极和共阴极接法的对比](https://blog.csdn.net/The_bad/article/details/130704983)
简单来讲就是stm32（数据手册 I/O port characteristics）**STM32的驱动电流最大为20mA，其==负载电流==有限**。其他单片机的负载电流也同样是有限的。如果采用共阴极接法，如果LED的驱动电流大于20mA，STM32的驱动效果就会很差，LED不亮或者很微弱。

### 如何配置GPIO功耗低
- [GPIO模式选择对低功耗的影响](https://www.wpgdadatong.com.cn/blog/detail/71252)
- [STM32低功耗模式下GPIO如何配置最节能？](https://bbs.huaweicloud.com/blogs/234482)
简单来讲就是尽量不要GPIO配置成悬空模式，不用做通信的引脚尽量设置低速等。


# 具体项目示例

## ADC&中断
- [使用STM32 HAL库驱动烟雾传感器的设计和优化](https://blog.csdn.net/weixin_66608063/article/details/134702311)

