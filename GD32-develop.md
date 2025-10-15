
- [我的gd32调试好的仓库](https://gitee.com/waaall/gd32-f470-vi-template.git)
- [STM32CUBEMX开发GD32F303](https://www.zhihu.com/column/c_1677010511353581568)

# vscode环境配置

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

