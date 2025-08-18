/* Bootloader启动文件 */
  .syntax unified
  .cpu cortex-m4
  .fpu softvfp
  .thumb

.global  Default_Handler

/* 链接器脚本定义的符号 */
.word  _sidata
.word  _sdata
.word  _edata
.word  _sbss
.word  _ebss

  .section  .text.Reset_Handler
  .weak  Reset_Handler
  .type  Reset_Handler, %function

/* Bootloader复位处理函数 */
Reset_Handler:
  movs r1, #0
  b DataInit

CopyData:
  ldr r3, =_sidata
  ldr r3, [r3, r1]
  str r3, [r0, r1]
  adds r1, r1, #4

DataInit:
  ldr r0, =_sdata
  ldr r3, =_edata
  adds r2, r0, r1
  cmp r2, r3
  bcc CopyData
  ldr r2, =_sbss
  b Zerobss

FillZerobss:
  movs r3, #0
  str r3, [r2], #4

Zerobss:
  ldr r3, = _ebss
  cmp r2, r3
  bcc FillZerobss

/* 调用SystemInit函数 */
  bl  SystemInit
/* 调用静态构造函数 */
  bl __libc_init_array
/* 调用Bootloader主函数 */
  bl bootloader_main
  bx lr
.size Reset_Handler, .-Reset_Handler

/* 默认中断处理函数 */
    .section .text.Default_Handler,"ax",%progbits
Default_Handler:
Infinite_Loop:
  b Infinite_Loop
  .size Default_Handler, .-Default_Handler

/* Bootloader向量表 */
   .section  .vectors,"a",%progbits
   .global __gVectors

__gVectors:
                    .word _sp                        /* 栈顶指针 */
                    .word Reset_Handler              /* 复位处理函数 */
                    .word NMI_Handler               /* NMI处理函数 */
                    .word HardFault_Handler         /* 硬件错误处理函数 */
                    .word MemManage_Handler         /* 内存管理错误 */
                    .word BusFault_Handler          /* 总线错误 */
                    .word UsageFault_Handler        /* 使用错误 */
                    .word 0                         /* 保留 */
                    .word 0                         /* 保留 */
                    .word 0                         /* 保留 */
                    .word 0                         /* 保留 */
                    .word SVC_Handler               /* SVC调用 */
                    .word DebugMon_Handler          /* 调试监控 */
                    .word 0                         /* 保留 */
                    .word PendSV_Handler            /* PendSV */
                    .word SysTick_Handler           /* SysTick定时器 */

  .size   __gVectors, . - __gVectors

/* 弱定义所有中断处理函数 */
  .weak NMI_Handler
  .thumb_set NMI_Handler,Default_Handler

  .weak HardFault_Handler
  .thumb_set HardFault_Handler,Default_Handler

  .weak MemManage_Handler
  .thumb_set MemManage_Handler,Default_Handler

  .weak BusFault_Handler
  .thumb_set BusFault_Handler,Default_Handler

  .weak UsageFault_Handler
  .thumb_set UsageFault_Handler,Default_Handler

  .weak SVC_Handler
  .thumb_set SVC_Handler,Default_Handler

  .weak DebugMon_Handler
  .thumb_set DebugMon_Handler,Default_Handler

  .weak PendSV_Handler
  .thumb_set PendSV_Handler,Default_Handler

  .weak SysTick_Handler
  .thumb_set SysTick_Handler,Default_Handler
