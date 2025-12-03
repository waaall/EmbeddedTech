
# Refs
- [Code Composer Studio IDE Guide](https://dev.ti.com/tirex/explore/content/mspm0_sdk_2_04_00_06/docs/english/tools/ccs_theia_ide_guide/doc_guide/doc_guide-srcs/ccs_theia_ide_guide.html)
- [MSPM0-SDK](https://www.ti.com.cn/tool/cn/MSPM0-SDK#tech-docs)
- [MSPM0 SDK DOC](https://software-dl.ti.com/msp430/esd/MSPM0-SDK/latest/docs/english/MSPM0_SDK_Documentation_Overview.html)
- [Ti ARM Clang](https://software-dl.ti.com/codegen/docs/tiarmclang/rel1_0_0_sts/tiarmclang_ug/tiarmclang-portfolio/index.html#)
- [theia和vscode](https://www.zhihu.com/question/383479657)


# CCSTUDIO
CCSTUDIO从Eclipse架构切换到Theia，2025年已完成切换，还是下载[CCSTUDIO](https://www.ti.com/tool/download/CCSTUDIO/)（目前更新到20.1版本，过渡的CCS Theia安装包不再更新）

## CCS/SDK/Sysconfig
CCSTUDIO、MSPM0SDK 和 SysConfig 是德州仪器（TI）针对微控制器（尤其是 MSPM0 系列）开发的工具链和软件组件，它们之间的关系如下：

---

### **1. CCSTUDIO（Code Composer Studio）**

- **定位**：TI 官方的集成开发环境（IDE），用于嵌入式软件开发。
- **功能**：
    - 提供代码编辑、编译、调试和仿真功能。
    - 支持多种 TI 处理器（包括 MSPM0、MSP430、C2000 等）。
- **与其他组件的关系**：
    - **MSPM0SDK**：CCSTUDIO 是 MSPM0SDK 的主要开发平台，可直接导入 SDK 中的示例工程。
    - **SysConfig**：集成 SysConfig 工具，用于图形化配置外设和生成代码。

---

### **2. MSPM0SDK**

- **定位**：TI 为 MSPM0 系列微控制器提供的软件开发套件（Software Development Kit）。
- **功能**：
    - 包含外设驱动库（DriverLib）、示例代码、RTOS 支持等。
    - 提供硬件抽象层（HAL）和板级支持包（BSP）。
- **与其他组件的关系**：
    - **CCSTUDIO**：SDK 的工程通常通过 CCSTUDIO 打开和编译。
    - **SysConfig**：SDK 依赖 SysConfig 生成外设初始化代码（如 GPIO、UART 等配置）。

---

### **3. SysConfig**

- **定位**：图形化配置工具，用于自动生成硬件外设和中间件的初始化代码。
- **功能**：
    - 通过可视化界面配置引脚复用、时钟、通信接口等。
    - 生成优化的 C 代码，减少手动编写底层配置的工作量。
- **与其他组件的关系**：
    - **CCSTUDIO**：作为插件集成在 CCSTUDIO 中，可直接在 IDE 内调用。
    - **MSPM0SDK**：SDK 中的示例工程通常包含 SysConfig 配置文件（`.syscfg`），用户可修改配置后重新生成代码。

---

### **三者的协作流程**

1. **开发环境**：用户在 CCSTUDIO 中创建或导入 MSPM0SDK 提供的工程。
2. **硬件配置**：通过 SysConfig 图形化配置外设（如 UART 波特率、GPIO 方向等），生成初始化代码。
3. **代码开发**：基于 SDK 的驱动库和 SysConfig 生成的代码，编写应用逻辑。
4. **编译调试**：使用 CCSTUDIO 编译、烧录和调试程序。

---

- **CCSTUDIO** 是核心开发环境。
- **MSPM0SDK** 提供软件资源（库和示例）。
- **SysConfig** 是辅助工具，简化硬件配置。  
    三者共同构成 TI MSPM0 开发的完整工具链，显著提高开发效率。

## vscode/cursor流程
当然还是要下载CCSTUDIO作为基本的配置工具的。但是可以使用`vscode/cursor + cortex-debug + arm-gcc + openocd + daplink/jlink` 来下载调试mspm0。

和stm的流程的核心区别在于openocd官方还未支持mspm0，ti已经开发了支持mspm0的openocd。据[官方帖子](https://e2e.ti.com/support/microcontrollers/arm-based-microcontrollers-group/arm-based-microcontrollers/f/arm-based-microcontrollers-forum/1373048/mspm0l1105-flashing-mspm0l1105-using-openocd)& [openocd分支来自Nishanth Menon](https://review.openocd.org/c/openocd/+/8385)。方法就是自己[github](https://github.com/nmenon/openocd/tree/master)下载并编译：
```bash
# 0. install deps (for example on ubuntu)
sudo apt update
sudo apt install git make autoconf automake libtool pkg-config libusb-dev libftdi1-dev libhidapi-dev

# 1. clone
mkdir openocd-mspm0
cd openocd-mspm0
git clone https://github.com/nmenon/openocd.git
cd openocd

# 2. prepare (like clone and make jimtcl)
./bootstrap
git submodule init
git submodule update
cd jimtcl
./configure
make
sudo make install

# 3. make (二进制文件/指令 的地址可以按需指定)
cd ..
./configure --prefix=/home/zx/Develop/openocd-mspm0
make
sudo make install

# 4. use dap (文件 cmsis-dap.cfg 和 ti_mspm0.cfg 也要指定位置或者拷贝到项目地址)
/home/zx/Develop/openocd-mspm0/bin/openocd  -f cmsis-dap.cfg -f ti_mspm0.cfg -c init -c "reset halt" -c "wait_halt" -c "flash write_image erase Debug/try_mspm0g3507.out" -c reset -c shutdown

# 5. debug 指定好cortex-debug插件的openocd地址就可以，或者在launch文件中指定
```



# 库函数

## driver lib介绍


## 0. RCC


## 1. Timer 


## 2. ADC


## 3. DAC


## 4. UART

### DMA

### FIFO


## 5. SPI

### DMA

### FIFO


## 6. I2C

### DMA

### FIFO



# 传感器

## 加速度传感器

### [mpu6050](https://github.com/Embedfire-sensor/ebf_sensor_mpu6050_data)
