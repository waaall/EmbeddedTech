 
- [我的gd32调试好的仓库](https://gitee.com/waaall/gd32-f470-vi-template.git)
- [STM32CUBEMX开发GD32F303](https://www.zhihu.com/column/c_1677010511353581568)

## vscode环境配置

vscode的环境配置，几乎就是相当于基于terminal的全开源流程。整体流程和stm32基本一致，就是交叉编译器用`make`+`arm-none-eabi-gcc`，烧录工具用`openocd` 或者`pyocd`（具体烧录硬件可以选stlink、jlink、gdlink、daplink，但有的可能需要安装驱动）。

与stm32不一样的几点：
- 库文件不一样，stm32有stm32cubeMX一键配置生成外设+库文件+makefile模版+各种所需，下文会细讲。`GD32EmbeddedBuilder_***\GD32EmbeddedBuilder\plugins\com.gigadevice.templatefwlib.arm.gd32f4xx_***\Firmware\`。这是跟gcc-make环境相关的库文件，并不是像网上说的不支持（可能后来支持了），而在官网下载的是firmware是适用于keil或者IAR的库文件。
- openocd最好用`GD32EmbeddedBuilder_***\Tools\OpenOCD\`这里的`scripts/target`有最新支持的ctg文件。
- mac 和 linux 建议用pyocd : `pip install pyocd`; 也可以用openocd,但需要一些trick: 改名字（gd32f4xx.ctg改为stm32f4xx.ctg）里面_CHIPNAME和_TARGETNAME改了就可以了。

另外，[GD32-DFP](https://gd32mcu.com/data/documents/pack/GigaDevice.GD32F4xx_DFP.3.0.3.pack)是keil的包，默认也是从这个网址下载，pyocd 也是在这里下载；下载失败可能是[gd32](https://gd32mcu.com)证书过期之类的，等等`pyocd pack update`再下载就好了。这个.pack文件其实就是zip文件，重命名后解压就会发现其中还是下面讲的这一套文件（CMSIS、startup、Peripheral Lib等）。具体操作见 [我的gd32调试好的仓库](https://gitee.com/waaall/gd32-f470-vi-template.git)的README。

### pyocd 

#### pyocd pack install location
- Linux: $HOME/.local/share/cmsis-pack-manager
- Mac: $HOME/Library/Application Support/cmsis-pack-manager
- Windows: 'C:\\Users\\$USER\\AppData\\cmsis-pack-manager'

#### pyocd xml error

问题：pyocd报错xml，因为svd文件头多了两个空格
```bash
➜  3.0.3-new ls
3.0.3.pack
➜  3.0.3-new mv 3.0.3.pack 3.0.3.zip  
➜  3.0.3-new ls
3.0.3  3.0.3.zip
➜  3.0.3-new cd 3.0.3    
➜  3.0.3 ls
Device  Flash  GigaDevice.GD32F4xx_DFP.pdsc  SVD
➜  3.0.3 cd SVD    
➜  SVD ls
GD32F403.SFR  GD32F403.svd  GD32F4xx.SFR  GD32F4xx.svd
➜  SVD sudo vim GD32F4xx.svd

# vim进入insert模式删了开头两个空格后 Esc :wq! 保存，再压缩成zip，重命名.pack
```


## stm32流程开发gd32


### 1. 寻找对应芯片

对于gd32，基本上是对stm32的一比一复刻，理解了上述知识后只需要一点点工作就可以了。

比如对于GD32F470VIT6，对照他们的外设资源，就可以确定最接近的就是STM32F429VIT6，具体字母代表什么，比如接口个数、封装等信息我就不展开说了，随便查一查就知道了。


### 2. 初始化代码/库文件

#### 2.1 STM32CubeMX初始化

这个就当作是在开发stm32就可以，初始化时钟、外设、中断等，然后生成MAKEFILE项目文件。

#### 2.2 下载gd32芯片相关文件

`GigaDevice.GD32F4xx_DFP.3.0.3.pack/Device/F4XX`中Source和Include文件夹中就有上文提到的那几个文件。

### 3. 核对定义

用vscode或者任何文本编辑器对比也可以，用下面指令也可以，我建议前者。

查看向量表位置与内容：
  - arm-none-eabi-objdump -h your.elf | grep -E "vectors|isr"
  - arm-none-eabi-objdump -D your.elf | sed -n '1,120p'  # 检查起始几项是否为 _estack/Reset_Handler
  
确认符号是否导出：
  - arm-none-eabi-nm your.elf | grep -E "_sidata|_sdata|_edata|_sbss|_ebss|_estack|__gVectors|g_pfnVectors"

运行期核对时钟：
  - 在 main 里调用 SystemCoreClockUpdate 后打印/断点检查 SystemCoreClock

核对芯片手册尤其是外设接口、寄存器定义是否一致。（不一致需要修改对应的库文件）

### 4. 修改中断向量表

也就是在`startup_gd32f4xx.s`中定义的中断向量表和中断向量处理函数名，要和stm32中一致，比如在gd32中DMA中断处理函数是这样命名的：

```
                    .word DMA0_Channel0_IRQHandler
                    .word DMA0_Channel1_IRQHandler
                    .word DMA0_Channel2_IRQHandler
                    .word DMA0_Channel3_IRQHandler
```

而在stm32中DMA中断处理函数是这样命名的：

```
  .word     DMA1_Stream0_IRQHandler
  .word     DMA1_Stream1_IRQHandler
  .word     DMA1_Stream2_IRQHandler
  .word     DMA1_Stream3_IRQHandler
```

绝大多数只是名称不一样，不一样的替换就可以，但要注意有些是没有的比如stm的SAI：
```
  .word     SAI1_IRQHandler     /* SAI1
```

gd32中没有定义，这个就不要改：
```
                    .word 0     /* Vector Number 103,Reserved */
```


### 5. 修改MAKEFILE

#### ASM项
```makefile
# ASM sources
ASM_SOURCES = \
# startup_stm32f429xx.s

# ASM sources
ASMM_SOURCES = \
startup_gd32f450_470.S
```
#### LD项
```makefile
# LDSCRIPT = STM32F429XX_FLASH.ld
LDSCRIPT = gd32f4xx_flash.ld
```

别的都不用改，就可以像make + arm-gcc + openocd/pyocd 一样开发了。

#### openocd 
对于openocd最好是用“假的”`stm32f4xx.cfg`，否则可能有兼容性问题，当然如果用`GD32EmbeddedBuilder`中的openocd也可以，但只有windows版。

```gd32f4xx.cfg
# GigaDevice GD32F4xx target
  
source [find target/swj-dp.tcl]
source [find mem_helper.tcl]

if { [info exists CHIPNAME] } {
set _CHIPNAME $CHIPNAME
} else {
set _CHIPNAME stm32f4xx
}

set _ENDIAN little

# Work-area is a space in RAM used for flash programming
# By default use 4kB

if { [info exists WORKAREASIZE] } {
set _WORKAREASIZE $WORKAREASIZE
} else {
set _WORKAREASIZE 0x1000
}

# Allow overriding the Flash bank size
if { [info exists FLASH_SIZE] } {
set _FLASH_SIZE $FLASH_SIZE
} else {
# autodetect size
set _FLASH_SIZE 0
}

#jtag scan chain
if { [info exists CPUTAPID] } {
set _CPUTAPID $CPUTAPID
} else {
set _CPUTAPID 0x2BA01477
}

swj_newdap $_CHIPNAME cpu -irlen 4 -ircapture 0x1 -irmask 0xf -expected-id $_CPUTAPID
dap create $_CHIPNAME.dap -chain-position $_CHIPNAME.cpu

if {[using_jtag]} {
jtag newtap $_CHIPNAME bs -irlen 5
}

set _TARGETNAME $_CHIPNAME.cpu

target create $_TARGETNAME cortex_m -endian $_ENDIAN -dap $_CHIPNAME.dap

$_TARGETNAME configure -work-area-phys 0x20000000 -work-area-size $_WORKAREASIZE -work-area-backup 0

# flash size will be probed
set _FLASHNAME $_CHIPNAME.flash
flash bank $_FLASHNAME stm32f2x 0x08000000 $_FLASH_SIZE 0 0 $_TARGETNAME

# JTAG speed should be <= F_CPU/6. F_CPU after reset is 8MHz, so use F_JTAG = 1MHz
adapter speed 1000

adapter srst delay 100
if {[using_jtag]} {
jtag_ntrst_delay 100
}

reset_config srst_nogate

if {![using_hla]} {
# if srst is not fitted use SYSRESETREQ to
# perform a soft reset
cortex_m reset_config sysresetreq
}
```

### 6. 总结

总之对于GD32F470VIT6只需要三步：

1. 修改`startup_gd32f4xx.s`文件中的中断处理函数；
2. 修改makefile中的ASM项和LD项。
3. openocd可能要改一下`stm.ctg`的文件。

就可以当作STM32F429VIT6完全走stm32的开发流程了。具体可以见我的一个[模版仓库](https://github.com/waaall/gd32-template)---CubeMX_BareMetal分支。


## 显示驱动


### 关于显存数据排列

这一切混乱都因为我们最终需要用一个顺序的一维的数组来表示可能被定义不同方向和起始点的二维坐标系。


#### 取模方向

首先，关于取模：是因为单片机内字节为基本存储单位，而不是bit，所以就要约好这个字节在像素的二维坐标系中，是y轴的8个bit 作为一个细节，还是x轴，于是有了横纵取模一说：

横向取模：按行（x 方向）分组，每 8 个水平像素组成 1 字节。

纵向取模：按列（y 方向）分组，每 8 个垂直像素组成 1 字节。

  
#### 原点位置

但这不是全部，那如果纵向取模，一般约定是左上角为原点还是左下角为原点？


当然极端情况是右上、右下也可被做为原点，甚至更极端，还可能是负增长。但这几乎不可能，因为这纯属没事找事儿。所以我们一般都假设左侧为x轴零点，往右为x坐标增加方向（符合习惯）


但上下有歧义，因为如果在左上，符合我们写字的顺序（先写左上角，所以作为index首，右下为增长方向），但是如果在左下，符合我们数学上的定义（y轴上为增）。


但大多数还是已左上为坐标原点，取模软件也是这样。所以对于左上为左边原点且纵向取模，定好的话，显存的数据写成 n个8bit/一字节 组成的 一维数组，是没有问题。

但如果这时候有一个显示器驱动以左下为坐标原点（y轴上增长）且纵向取模，那么不仅字节组显存数组的方式要变，字节中的bit还要反过来才行。

当然对于上位机，可以用各种矩阵运算工具或者库函数可以将所有y方向的bit 反过来就可以了。但对于单片机，一般就需要分开处理（字节的组合在y方向到过来，纵向取模的字节内部的bit也要反过来）才可以。

#### 增长方向

当然，有一种可能，字节内部的bit 不用反过来了，就是：  
    
- 字模：纵向取模，高位在上；
- LCD：page 从下往上，字节高位代表 page 内的“上”，  
    这时你只需要调整“page 映射（哪个 page 算顶部）”，字节内部 bit 不一定要再翻转。

**注意！所以高位在上，指的是可以正常显示像素的话，字节内的第**

因此更严谨的说法是：

在“左上原点 + y 向下”的字模要映射到“左下原点 + y 向上 + page 模式”的显存时，一般需要：

1. 按 y 方向（行块、page）翻转一次；
2. 再根据控制器对 bit 的定义，视情况决定是否翻转字节内部 bit 顺序。


#### 总结：

1. 取模方向（横/纵）
2. 原点位置（左上/左下）
3. 坐标增长方向（y 向上 / y 向下）
4. 字节内部 bit 顺序（bit7 在上还是在下）


这四个维度在“字模工具”和“LCD 控制器”两边往往不完全一致，

而要用一维字节数组去解决这一切差异，一旦任何一项没对齐，就会出现：

- 上下翻转
- 左右镜像
- 旋转 90°
- 图像像被“对折”了一样错位


#### 举例说明

假设屏幕纵向只有16个像素点。

如果屏幕左上为原点，像素显示如下：


```text
     x →
     0 1 2 3 4 5 6 7 8 9 
y 0  # # # # . . . . . .
  1  # . . . . . . . . . 
  2  # . . . . . . . . . 
  3  # # # # . . . . . . 
  4  # . . . . . . . . . 
  5  # . . . . . . . . . 
  6  # . . . . . . . . .
  7  # . . . . . . . . . 
  8  . . . . . . . . . . 
  9  . . . . . . . . . . 
 10  . . . . . . . . . .  
 11  . . . . . . . . . .  
 12  . . . . . . . . . . 
 13  . . . . . . . . . . 
 14  . . . . . . . . . .
 15  . . . . . . . . . . 

```

假设是纵向取模、高位在上，则字母F的字模数据为：

```c
// 10 列 × 16 行，纵向取模，高位在上
uint8_t Up_F[10 * 2] = {
    // x = 0
    0xFF, 0x00,
    // x = 1
    0x90, 0x00,
    // x = 2
    0x90, 0x00,
    // x = 3
    0x90, 0x00,
    // x = 4
    0x00, 0x00,
    // x = 5
    0x00, 0x00,
    // x = 6
    0x00, 0x00,
    // x = 7
    0x00, 0x00,
    // x = 8
    0x00, 0x00,
    // x = 9
    0x00, 0x00
};
```

假设是纵向取模、高位在上，则字母F的字模数据为：
```c
// 纵向取模，高位在下，左上原点 + y 向下
uint8_t Down_F[10 * 2] = {
    // x = 0
    0xFF, 0x00,
    // x = 1
    0x09, 0x00,
    // x = 2
    0x09, 0x00,
    // x = 3
    0x09, 0x00,
    // x = 4
    0x00, 0x00,
    // x = 5
    0x00, 0x00,
    // x = 6
    0x00, 0x00,
    // x = 7
    0x00, 0x00,
    // x = 8
    0x00, 0x00,
    // x = 9
    0x00, 0x00
};
```

如果没有做任何处理显示在坐标原点为左下的屏幕上：

Up_F:
```text
     x →
     0 1 2 3 4 5 6 7 8 9 
y15  . . . . . . . . . .
y14  . . . . . . . . . .
y13  . . . . . . . . . .
y12  . . . . . . . . . .
y11  . . . . . . . . . .
y10  . . . . . . . . . .
y9   . . . . . . . . . .
y8   . . . . . . . . . .
y7   # # # # . . . . . .
y6   # . . . . . . . . .
y5   # . . . . . . . . .
y4   # # # # . . . . . .
y3   # . . . . . . . . .
y2   # . . . . . . . . .
y1   # . . . . . . . . .
y0   # . . . . . . . . .
```

Down_F:
```text
     x →
     0 1 2 3 4 5 6 7 8 9 
y15  . . . . . . . . . . 
y14  . . . . . . . . . . 
y13  . . . . . . . . . . 
y12  . . . . . . . . . . 
y11  . . . . . . . . . . 
y10  . . . . . . . . . . 
 y9  . . . . . . . . . . 
 y8  . . . . . . . . . . 
 y7  # . . . . . . . . . 
 y6  # . . . . . . . . . 
 y5  # . . . . . . . . . 
 y4  # . . . . . . . . . 
 y3  # # # # . . . . . . 
 y2  # . . . . . . . . . 
 y1  # . . . . . . . . . 
 y0  # # # # . . . . . . 
```



如果正确处理后，显示在在坐标原点为左下的屏幕上：

```text
     x →
     0 1 2 3 4 5 6 7 8 9 
y15  # # # # . . . . . . 
y14  # . . . . . . . . . 
y13  # . . . . . . . . . 
y12  # # # # . . . . . .
y11  # . . . . . . . . . 
y10  # . . . . . . . . . 
 y9  # . . . . . . . . .
 y8  # . . . . . . . . . 
 y7  . . . . . . . . . . 
 y6  . . . . . . . . . . 
 y5  . . . . . . . . . . 
 y4  . . . . . . . . . .
 y3  . . . . . . . . . .
 y2  . . . . . . . . . . 
 y1  . . . . . . . . . . 
 y0  . . . . . . . . . .

```

什么叫正确处理呢？

如果是Up_F，只需要y的字节间反过来（也就是pages的index反过来），但如果是Down_F，还需要在上述基础上，再把字节中的bit反过来。


#### 取模工具

- [lvgl-fontconverter](https://lvgl.io/tools/fontconverter)
- [lvgl-fontconverter-github](https://github.com/lvgl/lv_font_conv?utm_source=chatgpt.com)
- [u8g2-用于嵌入式](https://github.com/olikraus/u8g2)
- [image2cpp](https://github.com/javl/image2cpp)

- [我自己的取模工具](https://github.com/waaall/just-some-code/blob/main/DataProcess/bitmap_generator.py)