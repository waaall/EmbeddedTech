UI的项目和个人尝试代码都移出该git仓库，到《Learn_Embedded》下面

[toc]

[Deepin GUI方案](https://www.jianshu.com/p/e871723f9460)。
# GUI中的G
GUI是G+UI，这个Graphics，包含着在最底层计算机室怎么处理“图像”的，也就是把各种各样的“形状”、“颜色”、“3D信息”转化成最终像素的过程。

这一过程的原理，往往会出现在《计算图形学》，3D建模等方向，而在UI设计方向，好像少有人懂。其实这恰恰是计算机行业成功的表现，就是封装，一层层的抽象，让开发者不知道具体实现的底层细节，来开发更宏大的项目。比如Linux中GUI的`G`就是[X Window](https://zh.wikipedia.org/wiki/X%E8%A6%96%E7%AA%97%E7%B3%BB%E7%B5%B1)，但这还需要显卡、显卡驱动及显卡API如[OpenGL](https://zh.wikipedia.org/wiki/OpenGL)；而在Mac上，`OpenGL`和`X Window`对应的就是`Metal`和`AppKit`，当然Apple在近几年逐渐使用`IOS`和`MacOS`统一的`SwiftUI`来代替`MacOS`的`Appkit`和`IOS`的`UIKit`。总之，我们平常所说的GUI：只是操作系统提供了G，并又在G的API上封装了UI这个API，我们利用UI的API写窗口和主逻辑代码的链接关系（一般由Signal表示）

一方面源于好奇心，另一方面，正如之前我再三强调，了解更底层的原理，会使得现在的工作更加清晰明了，游刃有余。我们就来看看GUI中的G：

# 设计模式

首先需要明确一点：**所有设计模式的根本目的是将UI和逻辑代码区分开来，让软件工程（中大型软件）逻辑清晰易读，合作愉快。**部分原因是由于UI框架其实很复杂，想让它变得简单，就更要“少与逻辑代码沟通”。

其次需要明确一点，就是**上述这个理想状态是不可能实现的**，所以就是尽可能地分离，所以很容易就可以想到，关于UI设计，比如布局、颜色、大小啥的在一个文件中，而UI和逻辑代码的通信在另一个文件中，主逻辑代码在单独文件中，这就是所谓的MVC模式——Model-View-Controller。

而由于Model有View如何变化的极致，View的变化又控制着Model（一般改变Model中某个对象的参数），所以Controller这个文件就很难写。于是，UI框架的工程师们日复一日刚出了自动检测View变化传递给Model的功能，于是有这种功能的App模式起了个新名字——MVVM。

> MVC和MVVM最直观的区别在于，MVC的model是单向的，输出给view就完事了，controller不知道view上的改变，而MVVM的model在view上改变，后台也会知道。

## MVC


## MVVM


# UI框架
上节说到，UI的App努力想要把代码按功能性分离来，但是这就涉及到一个核心问题：**对象间通信**。

其实这和[进程间通信](https://www.jianshu.com/p/c1015f5ffa74)有点点相似之处，作为操作系统，将不同的进程用独立的内存块储存，既保证了安全，又保证了稳定性，但是进程之间想要通信，这两块独立的内存又不能互相访问，这就是两难问题。

对象间通信不仅在UI设计中存在，但是在UI设计中尤为严重，因为UI框架的面向对象特性，复杂性，以至于我们用到的UI都是相当复杂层层继承的类实例（对象）。而又因为UI需要与逻辑代码尽可能分离却又相互依赖的特性，致使大量的对象间通信问题，而如何在效率和易用性上权衡，又有什么好点子来让“两者”双赢？这就需要深入到UI框架的实现逻辑中去一眼究竟了。。

一个网页可视化的项目](http://www.alloyteam.com/2019/07/h5-build-tool-pipeline/)、[如何区别一个 App 是 Native App， Web App 还是 Hybrid app](https://www.zhihu.com/question/23622875)

python可是可以做GUI的。[关于可视化的方案和具体python实现](https://leovan.me/cn/2018/05/cross-platform-gui-application-based-on-pyqt/)、[python对接c++Qt的一个库——PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)、2020年末除了PySide6，是个大版本更新！

与此同时**c++的Qt当然也更新为Qt6**！！！

## 几种跨平台UI框架
* [什么语言最适合做 GUI？ - liulun的回答 - 知乎](https://www.zhihu.com/question/276815517/answer/2357232999)


## 嵌入式UI开发工具
系统选Linux 还是 安卓？ 开发工具选 Qt 还是 Android Studio？
* [一种为 Linux ARM 设备构建跨平台 UI 的新方法 | Linux 中国 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/351207435)

目前还有一个Qt for mcu，首先它不是开源的，其次它是在STM32这种单片机平台，也就是非Linux系统，但该系统有更多成熟的选择，不知道今后会发展成什么样。

> [什么语言最适合做 GUI？ - kevinlq的回答 - 知乎 ](https://www.zhihu.com/question/276815517/answer/936044235) 
>
> 这是一个医疗App开发者，用Qt

## Qt
- [macOS桌面开发工具选择](https://www.bumblemeow.com/techtalk/#desktop-dev-tools)
将 Qt 用于商业软件的主要考虑因素是[定价](https://www.qt.io/pricing)。虽然可以在[LGPL](https://www.gnu.org/licenses/lgpl-3.0.en.html) 下使用 Qt，但 商业软件遵守 LGPL 可能很棘手。鉴于 OEDcoder 是一个闭源项目，我们不愿意在 LGPL 下使用 Qt，即使我们可以合法地这样做。此外，它在大多数平台上都没有原生的外观和感觉。
### Qt project

> [Qt Creator中的.pro文件的详解](https://blog.csdn.net/hebbely/article/details/66970821)
>
### 一些问题的总结
[Qt没有真正完美的无边框解决方案吗？ - 知乎](https://www.zhihu.com/question/66830111) 


### [PySide2](https://doc.qt.io/qtforpython/modules.html)（2021已为PySide6）
标题链接是官方文档，还有一个写的很不错的[中文博客](https://www.cnblogs.com/zach0812/category/1524140.html)

### 不错的pyside开源项目
- [Modern-Desktop-GUI](https://github.com/KhamisiKibet/24-Modern-Desktop-GUI)
- [Modern-Desktop-GUI youtube介绍](https://www.youtube.com/watch?v=JK-B-CT34EU)


- [Modern_GUI_PyDracula_PySide6_or_PyQt6](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)
- [上述项目youtube说明](https://www.youtube.com/watch?v=9DnaHg4M_AM&t=156s)

### pyside教程
- [pyside tutorials](https://www.pythonguis.com/tutorials/pyside6-creating-your-first-window/)
- 

### PyQt和PySide的区别

[PyQt5和PySide2的区别](https://www.zhihu.com/question/21237276)、

> [可以参考这篇文章](https://machinekoder.com/pyqt-vs-qt-for-python-pyside2-pyside/)、
>
> 目前PyQt是由一家小公司[Riverbank Computing](https://link.zhihu.com/?target=https%3A//riverbankcomputing.com)维护的，PyQt历史更长一些，比较稳定，开发社区也比较大，有相关的deploy工具；而PySide（又名Qt for Python）现由Qt公司维护，比PyQt更年轻一些。截至2019年，最新版本是PyQt5和PySide2。
>
> 其实他俩API挺相似的，最大的区别是License，PyQt是GPL协议，Qt for Python是LGPL协议，前者不能商用。目前从各方面来看PyQt速度更快、工具更齐全，个人觉得是开发时间比较早的原因，根据开源协议，Qt for Python的实现要避开PyQt已经实现部分的实现方法。但Qt for Python由Qt公司官方支持，而且开源可商用，目测未来发展会超越PyQt。
>
> 如果不确定用哪款，还有一种方法是加个中间层。有人对它们API做了包装，参见：[QtPy - Github](https://link.zhihu.com/?target=https%3A//github.com/spyder-ide/qtpy)
>
> 文档在这里：
>
> [Qt for Python - Qt for Pythondoc.qt.io](https://link.zhihu.com/?target=https%3A//doc.qt.io/qtforpython/)[PyQt5 Reference Guidewww.riverbankcomputing.com![图标](https://pic1.zhimg.com/v2-2eb7f384cad652e57235db5f4b9acf6c_ipico.jpg)](https://link.zhihu.com/?target=https%3A//www.riverbankcomputing.com/static/Docs/PyQt5/)
>
> （从文档看我还是倾向用Qt for Python的）

### pyside技术细节
见笔记《Learn Python-Qt》


## GUILite
- [GuiLite-github](https://github.com/idea4good/GuiLite)
- 