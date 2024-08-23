
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
- [OpenOCD](https://openocd.org/pages/getting-openocd.html)：用于烧录和调试。
- [STlink驱动](https://www.st.com.cn/zh/development-tools/stsw-link009.html)：用于烧录。
- **GCC & Make & git**：用于管理构建过程（可选，如果使用 `Makefile`）。不同操作系统的开发机器有所不同，windows安装mingw64，mac就是xcode，linux则是build-essential。
- vscode或者sublime用于写代码：更推荐vscode用来写一些有一定体量的工程化代码，sublime更轻量功能也更少一些。
#### vscode config
可以设置个`.vscode`文件夹，然后设置上`settings.json`、`c_cpp_properties.json`、`tasks.json`和`launch.json`。不用整这些，直接打开vscode中的terminal然后make就行（make和交叉编译的exe文件夹都要加入环境变量）。 
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


