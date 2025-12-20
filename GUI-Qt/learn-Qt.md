

## refs

- [qfluentwidgets](https://qfluentwidgets.com/zh/pages/about)
- [KDABtv-YouTube 频道](https://www.youtube.com/%40KDABtv)


## 关于Qt UI 的开发方式


### 1. Qt Widgets

这是 Qt 的传统桌面 UI 框架，一切都是 QWidget 派生类，主要用 C++（也可绑定到别的语言）。官方对它的定位就是“经典桌面风格界面”的一套 UI 元件库。 


### 2. Qt .ui

“.ui”不是第三套 UI 框架，它是给 Qt Widgets 用的“界面描述文件格式”。本质是 XML，把一个窗体里的控件树、布局、属性写在文件里。然后你有两种用法：

1 通过 uic 在编译期把 .ui 转成 C++ 代码再编译进程序

2 运行时用 QUiLoader 读取 XML 动态创建控件树 

  
所以：.ui 和 Widgets 的关系是“设计与生成方式”，离不开 Widgets。

  
### 3. QML Qt Quick

这是另一套 UI 技术栈。QML 是声明式语言，Qt Quick 是它的 UI 与渲染框架，强调动画、状态、过渡、触控交互等，最初就很面向移动与触控场景。 

  
依赖关系与能否混用

1 Widgets 与 QML 没有谁依赖谁，它们是并列的两套 UI 框架

2 .ui 依赖 Widgets（因为 .ui 描述的就是 widget 树） 

3 可以混用，但要选“谁是主框架”

- 在 Widgets 应用里嵌入 Qt Quick：用 QQuickWidget，或把 QQuickWindow 通过 createWindowContainer 放进 QWidget 布局里，官方有示例。 
- 反过来在 Qt Quick 应用里“嵌 Widgets”：不是主流路线，通常要另开窗口或用特定方案，整体体验和工程复杂度都更高（也更容易踩坑）


### 官方倾向与定位

官方文档对两者的核心区分很明确：

- Qt Quick 更偏动态界面、流畅动画、触控体验
- Qt Widgets 更偏桌面外观与桌面交互范式 

同时 Qt 官方也持续投入 Qt Quick 方向（例如 Qt Quick Controls 的桌面风格与原生化、Quick 与 Widgets 的桥接能力等），但 Widgets 依然是“经典桌面应用”的稳定选择。 


### 优缺点对比

#### 1 Qt Widgets（纯代码或配合 .ui）

优点
- 桌面应用成熟稳定，控件生态与传统桌面交互非常完整
- 更容易做“重数据”的桌面工具（表格、树、复杂表单、停靠面板等）
- 原生桌面风格更顺手（依赖 Qt 的样式系统与平台集成） 

缺点
- 做高度自定义外观、丝滑动画和复杂过渡通常更费劲
- 想要“现代感 UI”往往需要更重的样式与绘制工作

  

#### 2 .ui（Widgets 的设计方式）

优点
- 拖拽布局快，适合表单类界面；UI 与业务逻辑更分离
- 编译期生成代码性能开销小；也可运行时加载以支持皮肤化/插件化界面 

缺点
- XML 文件在多人协作时容易产生合并冲突
- 复杂动态 UI 仍然要回到代码里拼装；本质能力上限仍是 Widgets

#### 3 QML Qt Quick

优点
- 声明式写 UI，状态/动画/过渡/手势更自然，原生支持更“现代”的交互范式 
- 适合触控、嵌入式、需要大量动效或自定义外观的产品

缺点
- 需要适应 QML 的绑定、对象生命周期、性能最佳实践等，写法不当容易出现性能抖动（官方专门给了最佳实践） 
- 和 Widgets 混用时要注意桥接方案的限制与性能代价，比如 QQuickWidget 更灵活但会有性能开销，官方文档明确提示了这一点 
    




### Qt project

> [Qt Creator中的.pro文件的详解](https://blog.csdn.net/hebbely/article/details/66970821)


## 问题


### 一些问题的总结

- [Qt没有真正完美的无边框解决方案吗？ - 知乎](https://www.zhihu.com/question/66830111) 



