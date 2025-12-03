/*!
    \file    bootloader_main.c
    \brief   自定义Bootloader主程序

    \version 2025-08-12, V1.0.0, custom bootloader for GD32F4xx
*/

#include "gd32f4xx.h"
#include <stdint.h>

/* 应用程序起始地址 */
#define APP_START_ADDR    0x08004000UL
#define CONFIG_START_ADDR 0x0807F000UL

/* 升级标志定义 */
#define UPDATE_FLAG_ADDR  (CONFIG_START_ADDR + 0x00)
#define UPDATE_MAGIC      0x12345678UL
#define APP_VALID_MAGIC   0x87654321UL

/* 函数声明 */
void bootloader_main(void);
static void jump_to_application(uint32_t app_addr);
static uint8_t check_application_valid(uint32_t app_addr);
static void handle_firmware_update(void);
static void bootloader_gpio_init(void);
static void bootloader_usart_init(void);

/*!
    \brief    Bootloader主函数
    \param[in]  none
    \param[out] none
    \retval     none
*/
void bootloader_main(void)
{
    uint32_t update_flag;
    
    /* 初始化Bootloader外设 */
    bootloader_gpio_init();
    bootloader_usart_init();
    
    /* 检查升级标志 */
    update_flag = *(volatile uint32_t*)UPDATE_FLAG_ADDR;
    
    if (update_flag == UPDATE_MAGIC) {
        /* 需要升级固件 */
        handle_firmware_update();
        
        /* 清除升级标志 */
        // 这里需要Flash擦写操作
        
        /* 升级完成后检查应用程序 */
        if (check_application_valid(APP_START_ADDR)) {
            jump_to_application(APP_START_ADDR);
        }
    } else {
        /* 正常启动，检查应用程序是否有效 */
        if (check_application_valid(APP_START_ADDR)) {
            jump_to_application(APP_START_ADDR);
        }
    }
    
    /* 如果到达这里，说明应用程序无效，进入升级模式 */
    handle_firmware_update();
    
    /* 无限循环 */
    while(1) {
        /* Bootloader错误处理 */
    }
}

/*!
    \brief    跳转到应用程序
    \param[in]  app_addr: 应用程序起始地址
    \param[out] none
    \retval     none
*/
static void jump_to_application(uint32_t app_addr)
{
    uint32_t app_stack_pointer;
    uint32_t app_reset_handler;
    void (*app_entry)(void);
    
    /* 检查应用程序栈指针是否在有效范围内 */
    app_stack_pointer = *(volatile uint32_t*)app_addr;
    if ((app_stack_pointer < 0x20000000) || (app_stack_pointer > 0x20030000)) {
        return; /* 栈指针无效 */
    }
    
    /* 获取应用程序复位向量 */
    app_reset_handler = *(volatile uint32_t*)(app_addr + 4);
    
    /* 检查复位向量是否在应用程序Flash区域内 */
    if ((app_reset_handler < APP_START_ADDR) || (app_reset_handler > 0x08080000)) {
        return; /* 复位向量无效 */
    }
    
    /* 禁用所有中断 */
    __disable_irq();
    
    /* 重新配置向量表偏移 */
    SCB->VTOR = app_addr;
    
    /* 设置栈指针 */
    __set_MSP(app_stack_pointer);
    
    /* 跳转到应用程序 */
    app_entry = (void (*)(void))app_reset_handler;
    app_entry();
}

/*!
    \brief    检查应用程序是否有效
    \param[in]  app_addr: 应用程序起始地址
    \param[out] none
    \retval     uint8_t: 1-有效, 0-无效
*/
static uint8_t check_application_valid(uint32_t app_addr)
{
    uint32_t stack_pointer = *(volatile uint32_t*)app_addr;
    uint32_t reset_handler = *(volatile uint32_t*)(app_addr + 4);
    
    /* 检查栈指针是否在RAM范围内 */
    if ((stack_pointer < 0x20000000) || (stack_pointer > 0x20030000)) {
        return 0;
    }
    
    /* 检查复位向量是否在应用程序Flash范围内 */
    if ((reset_handler < APP_START_ADDR) || (reset_handler > 0x08080000)) {
        return 0;
    }
    
    /* 检查复位向量是否为奇数（Thumb指令） */
    if ((reset_handler & 0x01) == 0) {
        return 0;
    }
    
    return 1;
}

/*!
    \brief    处理固件升级
    \param[in]  none
    \param[out] none
    \retval     none
*/
static void handle_firmware_update(void)
{
    /* 这里实现固件升级逻辑 */
    /* 可以通过UART、USB、CAN等接口接收新固件 */
    /* 示例：通过UART接收固件数据并写入Flash */
    
    /* 1. 擦除应用程序区域 */
    /* 2. 接收固件数据 */
    /* 3. 写入Flash */
    /* 4. 校验固件完整性 */
    
    // 这里只是示例框架
}

/*!
    \brief    初始化Bootloader使用的GPIO
    \param[in]  none
    \param[out] none
    \retval     none
*/
static void bootloader_gpio_init(void)
{
    /* 启用GPIO时钟 */
    rcu_periph_clock_enable(RCU_GPIOG);
    
    /* 配置LED引脚 */
    gpio_mode_set(GPIOG, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO_PIN_6);
    gpio_output_options_set(GPIOG, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_6);
    
    /* 配置按键引脚 */
    rcu_periph_clock_enable(RCU_GPIOA);
    gpio_mode_set(GPIOA, GPIO_MODE_INPUT, GPIO_PUPD_PULLUP, GPIO_PIN_0);
}

/*!
    \brief    初始化Bootloader使用的USART
    \param[in]  none
    \param[out] none
    \retval     none
*/
static void bootloader_usart_init(void)
{
    /* 启用USART0时钟 */
    rcu_periph_clock_enable(RCU_GPIOA);
    rcu_periph_clock_enable(RCU_USART0);
    
    /* 配置USART0引脚 */
    gpio_af_set(GPIOA, GPIO_AF_7, GPIO_PIN_9);
    gpio_af_set(GPIOA, GPIO_AF_7, GPIO_PIN_10);
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_9);
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_10);
    
    /* 配置USART0参数 */
    usart_deinit(USART0);
    usart_baudrate_set(USART0, 115200U);
    usart_receive_config(USART0, USART_RECEIVE_ENABLE);
    usart_transmit_config(USART0, USART_TRANSMIT_ENABLE);
    usart_enable(USART0);
}
