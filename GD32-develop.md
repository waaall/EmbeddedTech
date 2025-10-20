 
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