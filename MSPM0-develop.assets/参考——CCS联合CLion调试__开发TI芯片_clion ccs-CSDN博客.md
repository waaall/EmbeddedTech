---
title: "参考——CCS联合CLion调试__开发TI芯片_clion ccs-CSDN博客"
source: "https://blog.csdn.net/m0_74349248/article/details/140450912"
author:
published:
created: 2025-04-02
description: "文章浏览阅读1.4k次，点赞26次，收藏24次。CCS联调CLion，开发TI芯片_clion ccs"
tags:
  - "clippings"
---
## 一、简介

随着[电赛](https://so.csdn.net/so/search?q=%E7%94%B5%E8%B5%9B&spm=1001.2101.3001.7020)临近，有些题必须指定使用TI芯片，那么就不得不学一下**CCS**。虽然[CCS](https://so.csdn.net/so/search?q=CCS&spm=1001.2101.3001.7020)相较于Keil和IAR，显得更**现代化**一些，但还是没有**代码样式**、**代码格式化**、**代码补全**等功能。如果你用惯了CLion再用CCS，就会有些许一言难尽，总得来说就是智能了但又没完全智能，比如断点。因此想到了使用**CLion**来开发TI芯片.

只不过过程很不顺，最主要的原因在于我使用的芯片是**MSPM0G3507**，且是**launchpad**，而**OpenOCD**上好像又没有相关的配置，最终导致调试TI开发板。想过直接使用GDB，或者换成可以使用**JLink**的开发板（有空再说），但由于时间有限就不得不找个次替方案，于是就想到了CCS联调**CLion**。

这里所谓的联调指的是在**CLion**里面编写代码（包括检测语法错误），在CCS里进行外设初始化、调试等，虽不如最初的构想，但也可以大大降低开发难度。同时，**CLion**有**Code with me**这个功能，这意味着你和其他人可以联合开发同一个项目。下面配置中最难的步骤在于“删”和配置CMakelists，由于我们使用的**TI芯片**可能不同，所以这里主要讲方法。

## 二、联调配置

### 1，工程创建

#### ①编译器选型

前面提到，既然要想**CCS**联调**CLion**，那么就必须把CCS相关工程配好，在不影响CCS编译的情况下，联调**CLion**。CCS一共有两个编译工具链，其一为**clang**，其二为**arm-gnu**，不过后者需要的版本是9.82，这与**CLion**用的版本多半不同且CCS需要自己配置arm-gnu工具链。

所以**CCS**的工程就选为**clang**，虽说与CLion用的编译器不同，语法、生成的代码会有些许差异，但是**CLion**在这里发挥的作用主要是编写，也就不用考虑了（有问题再说）。

#### ②导入工程

这里选用的是官方实例中的RTOS工程，首先要到官网下载相应的SDK，我使用的芯片是**MSPM0G3507**，所以就下载了MSPM0的SDK[MSPM0-SDK 软件开发套件 (SDK) | 德州仪器 TI.com.cn](https://www.ti.com.cn/tool/cn/MSPM0-SDK#downloads "MSPM0-SDK 软件开发套件 (SDK) | 德州仪器 TI.com.cn")

在SDK里，我们需要找到对应工程，它就在【**example-rtos-LP\_MSPM0G3507-kernel**】里。

我们选用最基础的闪灯工程。

![](https://i-blog.csdnimg.cn/direct/d4727aecb1c9479c9e5c2e6a9b3a37dd.png)

为了后续移植方便，把这个SDK复制到你准备创建的**workplace**里，我这里的workplace是TI这个目录，**Furina**是其工程名。

![](https://i-blog.csdnimg.cn/direct/1670413189ed4c62b534beb6a485c3f7.png)

在**CCS**里找到对应目录，直接导入即可

![](https://i-blog.csdnimg.cn/direct/05318af1dc6546249fe6a4a1aaf1a7c8.png)

然后你就会得到以下目录

![](https://i-blog.csdnimg.cn/direct/c11fb770116d424db264d89a1914175b.png)

### 2，准备CLion工程前置工作

#### ①编写CMakelists

前面提到这个工程名为Furina，那么在里面添加一个CMakelists.txt文件。这里面的编译器选项和链接器选项都是参照官方实例里gcc下的**Makefile**。这个嘛，就**看个人选择**，你可以直接使用官方这个**makefile**，配置相应的**Makefile程序**也是可以的，**这样反而更快**。不过由于我将来要尝试使用**OpenOCD**或者其他什么的调试程序，所以在此就用了最熟悉的cmake。

如果你想使用makefile（本篇文章省去了具体配置过程，不过过程并不难），那么就而可以直接跳到**【3，配置CLion工程】**

![](https://i-blog.csdnimg.cn/direct/8d3e7cde8d0a475f91bed346ca8152ad.png)

照着里面的**CFLAGS**和**LFLAGS**里的参数（比如**\-mthumb**）把对应的**add\_compile\_options**和**add\_link\_options**也改一下。同时要注意，CFLAGS里有个宏定义**\-D\_\_MSPM0G3507\_\_**，需要添加至**add\_definitions**里。

```cobol
set(CMAKE_SYSTEM_NAME Generic)

set(CMAKE_SYSTEM_VERSION 1)

cmake_minimum_required(VERSION 3.28)

 

#

#set(toolsPath /usr/arm-gnu-toolchain/bin)

#set(CMAKE_C_COMPILER ${toolsPath}/arm-none-eabi-gcc)

#set(CMAKE_CXX_COMPILER ${toolsPath}/arm-none-eabi-g++)

#set(CMAKE_ASM_COMPILER ${toolsPath}/arm-none-eabi-gcc)

#set(CMAKE_AR  ${toolsPath}/arm-none-eabi-ar)

#set(CMAKE_OBJCOPY  ${toolsPath}/arm-none-eabi-objcopy)

#set(CMAKE_OBJDUMP  ${toolsPath}/arm-none-eabi-objdump)

 

#下面代码是MinGW工具链下的

# specify cross-compilers and tools

set(CMAKE_C_COMPILER arm-none-eabi-gcc)

set(CMAKE_CXX_COMPILER arm-none-eabi-g++)

set(CMAKE_ASM_COMPILER arm-none-eabi-gcc)

set(CMAKE_AR arm-none-eabi-ar)

set(CMAKE_OBJCOPY arm-none-eabi-objcopy)

set(CMAKE_OBJDUMP arm-none-eabi-objdump)

set(SIZE arm-none-eabi-size)

 

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

 

# project settings

project(blink_led C CXX ASM)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_C_STANDARD 11)

 

#如果是FreeRTOS，那么下面需要开启，如果是RT-Thread，则需要关闭

#Uncomment for hardware floating point

#add_compile_definitions(ARM_MATH_CM4;ARM_MATH_MATRIX_CHECK;ARM_MATH_ROUNDING)

#add_compile_options(-mfloat-abi=hard -mfpu=fpv4-sp-d16)

#add_link_options(-mfloat-abi=soft -mfpu=fpv4-sp-d16)

 

#Uncomment for software floating point，要注释

add_compile_options(-mfloat-abi=soft)

 

#add_compile_options(-mcpu=cortex-m0plus -mthumb -mthumb-interwork)

#add_compile_options(-ffunction-sections -fdata-sections -fno-common -fmessage-length=0)

add_compile_options(-mcpu=cortex-m0plus -march=armv6-m -mthumb -mthumb-interwork)

add_compile_options(-ffunction-sections -fdata-sections -fno-common -fmessage-length=0 -gstrict-dwarf)

# Enable assembler files preprocessing

add_compile_options($<$<COMPILE_LANGUAGE:ASM>:-x$<SEMICOLON>assembler-with-cpp>)

 

 

add_link_options(-Wl,-gc-sections,--print-memory-usage,-Map=${PROJECT_BINARY_DIR}/${PROJECT_NAME}.map)

add_link_options(-mcpu=cortex-m0plus -march=armv6-m -mthumb -mthumb-interwork)

add_link_options(-T ${LINKER_SCRIPT})

 

# uncomment to mitigate c++17 absolute addresses warnings

#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-register")

 

 

if ("${CMAKE_BUILD_TYPE}" STREQUAL "Release")

    message(STATUS "Maximum optimization for speed")

    add_compile_options(-Ofast)

elseif ("${CMAKE_BUILD_TYPE}" STREQUAL "RelWithDebInfo")

    message(STATUS "Maximum optimization for speed, debug info included")

    add_compile_options(-Ofast -g)

elseif ("${CMAKE_BUILD_TYPE}" STREQUAL "MinSizeRel")

    message(STATUS "Maximum optimization for size")

    add_compile_options(-Os)

else ()

    message(STATUS "Minimal optimization, debug info included")

    add_compile_options(-Og -g)

endif ()

 

add_definitions(-DDEBUG -D__MSPM0G3507__)

 

include_directories(

        ticlang/Application

        ticlang/Debug

 

        kernel/freertos/builds/LP_MSPM0G3507/release

        source/third_party/CMSIS/Core/Include

        source/third_party/CMSIS/DSP/Include

        source/third_party/CMSIS/DSP/PrivateInclude

        kernel/freertos/Source/include

        source

        kernel/freertos/Source/portable/GCC/ARM_CM0

        source/ti/posix/gcc

 

        source/third_party/mcuboot/boot/bootutil/include

)

 

file(GLOB_RECURSE SOURCES

        "ticlang/Application/*.*"

        "ticlang/Debug/ti_msp_dl_config.c"

        "ticlang/Debug/ti_msp_dl_config.h"

 

        "kernel/freertos/builds/LP_MSPM0G3507/release/*.*"

        "kernel/freertos/Source/portable/GCC/ARM_CM0/*.*"

        "kernel/freertos/Source/include/*.*"

        "kernel/freertos/Source/*.*"

        "kernel/freertos/dpl/*.*"

 

        "source/*.*"

    "syscalls.c"

)

#下面是额外添加的，用于动态代码的分析

#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address")

 

#set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/STM32F407VETX_FLASH.ld)

set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/mspm0g3507.lds)

 

 

 

add_executable(${PROJECT_NAME}.elf ${SOURCES} ${LINKER_SCRIPT})

 

set(HEX_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.hex)

set(BIN_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.bin)

 

add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD

        COMMAND ${CMAKE_OBJCOPY} -Oihex $<TARGET_FILE:${PROJECT_NAME}.elf> ${HEX_FILE}

        COMMAND ${CMAKE_OBJCOPY} -Obinary $<TARGET_FILE:${PROJECT_NAME}.elf> ${BIN_FILE}

        COMMENT "Building ${HEX_FILE}

Building ${BIN_FILE}")
```

#### ②添加链接文件

这个还是到gcc那个文件夹，把这个**lds文件**添加至**Furina**工程里。添加这个是为了可以在使用**CLion**构建时看到程序**大致**占用情况（clang编译器与gcc终归不一样，所以会和实际有些出入）

![](https://i-blog.csdnimg.cn/direct/35d457902e5c4313ab06acbd05e29ac0.png)

### 3，配置CLion工程

接下来先导包，呃我的意思是向**Furina**这个工程SDK里的两个库，一个是**source**，另一个是**kernel**

![](https://i-blog.csdnimg.cn/direct/f9c2f3853d134fc8a604894720e89ea8.png)![](https://i-blog.csdnimg.cn/direct/164375704b1247798fcdca67c20548fc.png)

然后直接右键**Furina**这个文件夹用**CLion**打开，添加**cmake**项目之类的相信你已经炉火纯青了。

第一次编译的时候会报许多错，原因有三

其一为“添加的这个**source**和**kernel**库里有脏东西”，比如说下面这个目录里会有IAR、MemMang等不相关的东西。除了**GCC**都应该把它删掉，这个需要自己对应报错提示去修改，同时配合**CMakelists**里设置的包含目录和资源文件，过程比较繁琐耗时

![](https://i-blog.csdnimg.cn/direct/0dfe711f039741ba9fab64abd8907847.png)

需要的文件可以参考下面的release文件夹

![](https://i-blog.csdnimg.cn/direct/7e7dd77bceca46fc86ede7ff9fb96504.png)

其二为 “缺少相关定义——unfined”，添加个**syscalls.c**就行了，代码如下（\_sbrk可能需要你改，可参照lds链接脚本文件）。同时，不要直接放到Furina工程的**ticlang**（显示**Active Debug**的那个目录，我重命名过）里，不然**CCS**会自动编译它导致构建错误，这里推荐放在外面，

![](https://i-blog.csdnimg.cn/direct/2809ad57e5cf42a7b9e025178646fb06.png)

再在链接脚本文件里添加了一句

```cpp
_estack = ORIGIN(SRAM) + LENGTH(SRAM);
```

![](https://i-blog.csdnimg.cn/direct/723bf7b763c249a78f714b358e394424.png)

```cpp
/**

 ******************************************************************************

 * @file      syscalls.c

 * @author    Auto-generated by STM32CubeIDE

 * @brief     STM32CubeIDE Minimal System calls file

 *

 *            For more information about which c-functions

 *            need which of these lowlevel functions

 *            please consult the Newlib libc-manual

 ******************************************************************************

 * @attention

 *

 * Copyright (c) 2020-2024 STMicroelectronics.

 * All rights reserved.

 *

 * This software is licensed under terms that can be found in the LICENSE file

 * in the root directory of this software component.

 * If no LICENSE file comes with this software, it is provided AS-IS.

 *

 ******************************************************************************

 */

 

/* Includes */

#include <sys/stat.h>

#include <stdlib.h>

#include <errno.h>

#include <stdio.h>

#include <signal.h>

#include <time.h>

#include <sys/time.h>

#include <sys/times.h>

 

 

/* Variables */

extern int __io_putchar(int ch) __attribute__((weak));

extern int __io_getchar(void) __attribute__((weak));

 

 

char *__env[1] = { 0 };

char **environ = __env;

 

 

/* Functions */

void initialise_monitor_handles()

{

}

 

int _getpid(void)

{

  return 1;

}

 

int _kill(int pid, int sig)

{

  (void)pid;

  (void)sig;

  errno = EINVAL;

  return -1;

}

 

void _exit (int status)

{

  _kill(status, -1);

  while (1) {}    /* Make sure we hang here */

}

 

__attribute__((weak)) int _read(int file, char *ptr, int len)

{

  (void)file;

  int DataIdx;

 

  for (DataIdx = 0; DataIdx < len; DataIdx++)

  {

    *ptr++ = __io_getchar();

  }

 

  return len;

}

 

__attribute__((weak)) int _write(int file, char *ptr, int len)

{

  (void)file;

  int DataIdx;

 

  for (DataIdx = 0; DataIdx < len; DataIdx++)

  {

    __io_putchar(*ptr++);

  }

  return len;

}

 

int _close(int file)

{

  (void)file;

  return -1;

}

 

 

int _fstat(int file, struct stat *st)

{

  (void)file;

  st->st_mode = S_IFCHR;

  return 0;

}

 

int _isatty(int file)

{

  (void)file;

  return 1;

}

 

int _lseek(int file, int ptr, int dir)

{

  (void)file;

  (void)ptr;

  (void)dir;

  return 0;

}

 

int _open(char *path, int flags, ...)

{

  (void)path;

  (void)flags;

  /* Pretend like we always fail */

  return -1;

}

 

int _wait(int *status)

{

  (void)status;

  errno = ECHILD;

  return -1;

}

 

int _unlink(char *name)

{

  (void)name;

  errno = ENOENT;

  return -1;

}

 

int _times(struct tms *buf)

{

  (void)buf;

  return -1;

}

 

int _stat(char *file, struct stat *st)

{

  (void)file;

  st->st_mode = S_IFCHR;

  return 0;

}

 

int _link(char *old, char *new)

{

  (void)old;

  (void)new;

  errno = EMLINK;

  return -1;

}

 

int _fork(void)

{

  errno = EAGAIN;

  return -1;

}

 

int _execve(char *name, char **argv, char **env)

{

  (void)name;

  (void)argv;

  (void)env;

  errno = ENOMEM;

  return -1;

}

static uint8_t *__sbrk_heap_end = NULL;

 

/**

 * @brief _sbrk() allocates memory to the newlib heap and is used by malloc

 *        and others from the C library

 *

 * @verbatim

 * ############################################################################

 * #  .data  #  .bss  #       newlib heap       #          MSP stack          #

 * #         #        #                         # Reserved by _Min_Stack_Size #

 * ############################################################################

 * ^-- RAM start      ^-- _end                             _estack, RAM end --^

 * @endverbatim

 *

 * This implementation starts allocating at the '_end' linker symbol

 * The '_Min_Stack_Size' linker symbol reserves a memory for the MSP stack

 * The implementation considers '_estack' linker symbol to be RAM end

 * NOTE: If the MSP stack, at any point during execution, grows larger than the

 * reserved size, please increase the '_Min_Stack_Size'.

 *

 * @param incr Memory size

 * @return Pointer to allocated memory

 */

void *_sbrk(ptrdiff_t incr)

{

    extern uint8_t _end; /* Symbol defined in the linker script */

    extern uint8_t _estack; /* Symbol defined in the linker script */

    extern uint32_t _Min_Stack_Size; /* Symbol defined in the linker script */

    const uint32_t stack_limit = (uint32_t)&_estack - (uint32_t)&_Min_Stack_Size;

    const uint8_t *max_heap = (uint8_t *)stack_limit;

    uint8_t *prev_heap_end;

 

    /* Initialize heap end at first call */

    if (NULL == __sbrk_heap_end)

    {

        __sbrk_heap_end = &_end;

    }

 

    /* Protect heap from growing into the reserved MSP stack */

    if (__sbrk_heap_end + incr > max_heap)

    {

        errno = ENOMEM;

        return (void *)-1;

    }

 

    prev_heap_end = __sbrk_heap_end;

    __sbrk_heap_end += incr;

 

    return (void *)prev_heap_end;

}
```

第三个为“缺少**ti\_msp\_dl\_config**文件”，这个是**CCS**在Debug里产生的配置文件，复制到一个合适的位置就行（CMakelists要能找到）。或者直接把这个目录里的这两个文件包含进**CMakelists**里，后者这个更推荐，因为配置文件会经常改

![](https://i-blog.csdnimg.cn/direct/55f8518bdc0140bfb805fabb7c1428e6.png)

![](https://i-blog.csdnimg.cn/direct/182ba70a71524e0394f0088ee1482f84.png)

那么接下来除了一些小警告意外，就可以正常使用**CLion**来编写代码了，**CLion**这里可以检查语法错误，同时也不耽误**CCS**编译调试程序，开发体验也上去了，三赢零亏。

![](https://i-blog.csdnimg.cn/direct/e895f5c8c10549b1ba6ab80ff3cb1843.png)

## 三，可能用到的文档

### 1，TI的FFT官方文档

[bing.com/ck/a?!&&p=88d3645f0a6dc0d5JmltdHM9MTcyMTAwMTYwMCZpZ3VpZD0yNTgzZDVmYi03NjJkLTY1MDktMGNkNS1jMTQwNzc1ZTY0NDUmaW5zaWQ9NTE4Nw&ptn=3&ver=2&hsh=3&fclid=2583d5fb-762d-6509-0cd5-c140775e6445&psq=TI+FFT&u=a1aHR0cHM6Ly93d3cudGkuY29tL2NuL2xpdC9wZGYvemhjYTQxNA&ntb=1](https://www.bing.com/ck/a?!&&p=88d3645f0a6dc0d5JmltdHM9MTcyMTAwMTYwMCZpZ3VpZD0yNTgzZDVmYi03NjJkLTY1MDktMGNkNS1jMTQwNzc1ZTY0NDUmaW5zaWQ9NTE4Nw&ptn=3&ver=2&hsh=3&fclid=2583d5fb-762d-6509-0cd5-c140775e6445&psq=TI+FFT&u=a1aHR0cHM6Ly93d3cudGkuY29tL2NuL2xpdC9wZGYvemhjYTQxNA&ntb=1 "bing.com/ck/a?!&&p=88d3645f0a6dc0d5JmltdHM9MTcyMTAwMTYwMCZpZ3VpZD0yNTgzZDVmYi03NjJkLTY1MDktMGNkNS1jMTQwNzc1ZTY0NDUmaW5zaWQ9NTE4Nw&ptn=3&ver=2&hsh=3&fclid=2583d5fb-762d-6509-0cd5-c140775e6445&psq=TI+FFT&u=a1aHR0cHM6Ly93d3cudGkuY29tL2NuL2xpdC9wZGYvemhjYTQxNA&ntb=1")

![](https://i-blog.csdnimg.cn/direct/fec1072cf3e94b0d9469b8651d88a559.png)