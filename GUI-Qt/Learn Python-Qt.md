# 前言-Python-Qt

## 不错的pyside开源项目
- [Modern-Desktop-GUI](https://github.com/KhamisiKibet/24-Modern-Desktop-GUI)
- [Modern-Desktop-GUI youtube介绍](https://www.youtube.com/watch?v=JK-B-CT34EU)

- [Modern_GUI_PyDracula_PySide6_or_PyQt6](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)
- [上述项目youtube说明](https://www.youtube.com/watch?v=9DnaHg4M_AM&t=156s)


## pyside教程
- [pyside计算器](https://cloud.tencent.com/developer/article/2334289)
- [pyside官方教程](https://doc.qt.io/qtforpython-6/)

- [《Create GUI Applications with PySide6 Edition5》](https://www.pythonguis.com/tutorials/)
- [PySide6-Code-Tutorial](https://github.com/muziing/PySide6-Code-Tutorial)

- [PyQt_practice](https://github.com/muziing/PyQt_practice)

## PyQt和PySide的区别

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
> [Qt for Python - Qt for Pythondoc.qt.io](https://link.zhihu.com/?target=https%3A//doc.qt.io/qtforpython/)[PyQt5 Reference Guidewww.riverbankcomputing.com![图标](https://pic1.zhimg.com/v2-2eb7f384cad652e57235db5f4b9acf6c_ipico.jpg)](https://link.zhihu.com/?target=https%3A//www.riverbankcomputing.com/static/Docs/PyQt5/)
> （从文档看我还是倾向用Qt for Python的）
> 


## vscode写pyqt
- [VSCode插件"PYQT Integration" 和 "Qt for Python"的区别](https://juejin.cn/post/7319541565319348275)
下载插件-Qt for Python


# 技术框架

## 如何做好模块化？
- [Qt 中的 Model/View 结构](https://muzing.top/posts/5ff61cbd/)
什么时候用类？当几个函数具有明显的可扩展性和通用性时，无疑是需要类风装的，这样你可以作为副类让其他类继承这种通用性的函数，比如说一些基本的文件处理批量的重命名，在你整个科研过程中都要用到，不仅是处理图片还是处理数据还是处理什么东西都要用到类似的函数，那你可以把这一个函数封装到一个积累中，比如说就是file handler 然后图像处理的可以继承它用他的函数。

还有一种情况就是该文件(模块) 即使没有太多通用性，但是有一些所有函数都需要用到的全局变量，当然也可以把它作为局部变量传来传去，如果是数字或者字符串这种不大的数据也倒是可以，但是比如一个数组或者是一个对象可能就要作为全局变量，这种时候多文件管理起来就很多问题，不如把这个文件中的函数和全局变量都放到一个类里，此时这些函数依然可以调用改变量，但是是在这个对象内部。

对此chatgpt举了一个例子，还是可以的，如下！
在多个函数间共享状态的场景通常涉及到这些函数需要访问和修改相同的数据或属性。如果将这些函数封装在一个类中，可以通过类的实例属性来共享和管理这些状态。以下是一个具体的例子，展示了在多个函数间共享状态的情况。
### 何时用类---图片处理为例
假设你正在编写一个图片处理应用程序，涉及到加载图片、应用滤镜、调整亮度、以及保存图片的功能。这些操作都需要访问和修改相同的图片数据。
#### 1. 使用全局变量和独立函数（不共享状态的方式）
```python
import numpy as np
from PIL import Image, ImageEnhance

def load_image(file_path):
    global img
    img = Image.open(file_path)
    print("Image loaded.")

def apply_filter(filter_type):
    global img
    if filter_type == "grayscale":
        img = img.convert("L")
        print("Grayscale filter applied.")
    elif filter_type == "invert":
        img = Image.fromarray(np.invert(np.array(img)))
        print("Invert filter applied.")

def adjust_brightness(factor):
    global img
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(factor)
    print("Brightness adjusted.")

def save_image(output_path):
    global img
    img.save(output_path)
    print("Image saved.")
```

在这种情况下，`img` 是一个全局变量，在多个函数之间共享和修改。这种方式在简单的脚本中可能是有效的，但存在以下问题：

- **易出错**：全局变量容易被意外修改，导致难以调试的错误。
- **难以维护**：随着代码复杂性的增加，管理全局状态变得困难。

#### 2. 使用类共享状态
通过将这些功能封装在一个类中，图片数据 (`img`) 可以作为类的实例属性在多个方法之间共享。

```python
import numpy as np
from PIL import Image, ImageEnhance

class ImageProcessor:
    def __init__(self, file_path):
        self.img = Image.open(file_path)
        print("Image loaded.")

    def apply_filter(self, filter_type):
        if filter_type == "grayscale":
            self.img = self.img.convert("L")
            print("Grayscale filter applied.")
        elif filter_type == "invert":
            self.img = Image.fromarray(np.invert(np.array(self.img)))
            print("Invert filter applied.")

    def adjust_brightness(self, factor):
        enhancer = ImageEnhance.Brightness(self.img)
        self.img = enhancer.enhance(factor)
        print("Brightness adjusted.")

    def save_image(self, output_path):
        self.img.save(output_path)
        print("Image saved.")

# 使用示例
processor = ImageProcessor("input_image.jpg")
processor.apply_filter("grayscale")
processor.adjust_brightness(1.5)
processor.save_image("output_image.jpg")
```

在这个例子中，`ImageProcessor` 类的每个方法都可以访问和修改 `self.img`，这是一个类实例的属性。这样做的好处包括：

- **状态封装**：`img` 的状态被封装在 `ImageProcessor` 类的实例中，不会被全局变量污染。
- **易于扩展**：如果将来需要添加新的方法或属性，可以很容易地扩展 `ImageProcessor` 类，而无需担心全局状态的管理。
- **更好的代码组织**：通过类将相关功能封装在一起，使代码更有组织性，易于理解和维护。
#### 总结
通过类来共享状态，可以使代码更加模块化和结构化，减少全局变量的使用，降低错误的风险，并提高代码的可维护性。这种方法特别适用于需要在多个函数之间共享和修改相同数据的场景。

## UI files
Both packages use slightly different approaches for loading `.ui` files exported from Qt Creator/Designer. PyQt5 provides the `uic` submodule which can be used to load UI files directly, to produce an object. This feels pretty Pythonic (if you ignore the camelCase).

```python
import sys
from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("mainwindow.ui")
window.show()
app.exec()
```

The equivalent with PySide2 is one line longer, since you need to create a `QUILoader`object first. Unfortunately the api of these two interfaces is different too (`.load` vs `.loadUI`) and take different parameters.

```python
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

loader = QUiLoader()

app = QtWidgets.QApplication(sys.argv)
window = loader.load("mainwindow.ui", None)
window.show()
app.exec_()
```

To load a UI onto an object in PyQt5, for example in your `QMainWindow.__init__`, you can call `uic.loadUI` passing in `self` (the target widget) as the second parameter. 

```python
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
```

The PySide2 loader does not support this — the second parameter to `.load` is the *parent* widget of the widget you're creating. This prevents you adding custom code to the `__init__` block of the widget, but you can work around this with a separate function.

```python
import sys
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader

loader = QUiLoader()

def mainwindow_setup(w):
    w.setTitle("MainWindow Title")

app = QtWidgets.QApplication(sys.argv)

window = loader.load("mainwindow.ui", None)
mainwindow_setup(window)
window.show()
app.exec()
```

### Converting UI files to Python

Both libraries provide identical scripts to generate Python importable modules from Qt Designer `.ui` files. For PyQt5 the script is named `pyuic5` —



```bash
pyuic5 mainwindow.ui -o MainWindow.py
```

You can then import the `UI_MainWindow` object, subclass using multiple inheritance from the base class you're using (e.g. `QMainWIndow`) and then call `self.setupUI(self)` to set the UI up.

```python
import sys
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
```

For PySide2 it is named `pyside2-uic` —

```bash
pyside2-uic mainwindow.ui -o MainWindow.py
```

The subsequent setup is identical.

```python
import sys
from PySide2 import QtWidgets
from MainWindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
```



For more information on using Qt Designer with either PyQt5 or PySide2 see the [Qt Creator tutorial](https://www.learnpyqt.com/courses/qt-creator/).

### exec() or exec_()

The `.exec()` method is used in Qt to start the event loop of your `QApplication` or dialog boxes. In Python 2.7 `exec` was a keyword, meaning it could not be used for variable, function or method names. The solution used in both PyQt4 and PySide was to rename uses of `.exec` to `.exec_()` to avoid this conflict.

Python 3 removed the `exec` keyword, freeing the name up to be used. As PyQt5 targets only Python 3 it could remove the workaround, and `.exec()` calls are named just as in Qt itself. However, the `.exec_()` names are maintained for backwards compatibility.

PySide2 is available on both Python 3 and Python 2.7 and so still uses `.exec_()`. It is however only available for 64bit Linux and Mac.

If you're targeting both PySide2 and PyQt5 use `.exec_()`

## 布局

 给QWidget或者QDialog设置布局的时候方式很简单。创建好一个布局：mainLayout，然后不停地把各个控件往mainLayout里面放，最后调用setLayout(mainLayout)就行了。  QMainWindow中使用这个方法的时候却不管用，因为QMainWindow是默认有layout的，所以再次设置layout会失效。

 会出现这种提示：

 QWidget::setLayout: Attempting to set QLayout "" on MainWindow "", which already has a layout 这句话的意思是说，你已经给MainWindow设置过一个布局了，再设置一个会出错。  该如何给QMainWindow正确地设置布局呢 要想QMainWidget创建布局，合理的步骤应该是这样的：  第一步创建一个QWidget实例，并将这个实例设置为centralWidget：  然后创建一个主布局mainLayout，并把所需要的所有控件都往里面放（工具栏、菜单栏、状态栏除外）：  ...

最一步就是将widget的布局设置为mainLayout。

```python
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Mainwin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.createMenu()

    def setupUI(self):

        CenterWidget = self.setCentralWidget(Center())
        self.setDock()
        self.setWindowTitle("摩擦和热导率自动化")

    def createMenu(self):
        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction("copy")
        self.fileMenu.addAction("paste")
        self.fileMenu.addAction("save")
        self.fileMenu.addAction("save as")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction("Switch layout direction")


    def setDock(self):
        self.fileTree = QDockWidget()
        self.fileTree.setWindowTitle('Bookmarks')
        self.fieltree_widget = FileTreeWidget()
        self.fileTree.setWidget(self.fieltree_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.fileTree)

class Center(QWidget):

    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super().__init__()
        
        self.createHorizontalGroupBox()
        self.createGridGroupBox()
        self.createFormGroupBox()

        bigEditor = QTextEdit()
        bigEditor.setPlainText("This widget takes up all the remaining space "
                "in the top-level layout.")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Layouts")

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()

        for i in range(self.NumButtons):
            button = QPushButton("Button %d" % (i + 1))
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def createGridGroupBox(self):
        self.gridGroupBox = QGroupBox("Grid layout")
        layout = QGridLayout()

        for i in range(self.NumGridRows):
            label = QLabel("Line %d:" % (i + 1))
            lineEdit = QLineEdit()
            layout.addWidget(label, i + 1, 0)
            layout.addWidget(lineEdit, i + 1, 1)

        self.smallEditor = QTextEdit()
        self.smallEditor.setPlainText("This widget takes up about two thirds "
                "of the grid layout.")

        layout.addWidget(self.smallEditor, 0, 2, 4, 1)

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        self.gridGroupBox.setLayout(layout)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Line 1:"), QLineEdit())
        layout.addRow(QLabel("Line 2, long text:"), QComboBox())
        layout.addRow(QLabel("Line 3:"), QSpinBox())
        self.formGroupBox.setLayout(layout)
```



### 盒布局

### [Grid布局](https://www.cnblogs.com/zach0812/p/11401724.html)


## 多界面跳转

**问题1: ** 多数信号都已经定义好了，比如pushbutton，但是对于button触发的界面跳转，为什么还要自定义信号`pyqtSignal`呢？


**问题2：**这个类本身继承于Ui_Form类，但又把它的对象传入了它的父类Ui_Form？？？？


**问题3:** ObjectName是干什么的？

```python
self.auto_login_checkBox = QtWidgets.QCheckBox(self.widget_3)

self.auto_login_checkBox.setObjectName("auto_login_checkBox")

self.gridLayout.addWidget(self.auto_login_checkBox, 2, 0, 1, 1)
```

ObjectName主要是用于外界来访问内部的控件成员的，如果外界不需要访问这个成员，则理论上无需设置它的ObjectName。


## 事件和信号

[信号与槽](https://www.cnblogs.com/lsgxeva/p/12636756.html)、[自定义信号](https://www.cnblogs.com/zach0812/p/11406892.html)、

![自定义信号](learn-GUI.assets/自定义信号.png)

Defining custom slots and signals uses slightly different syntax between the two libraries. PySide2 provides this interface under the names `Signal` and `Slot` while PyQt5 provides these as `pyqtSignal` and `pyqtSlot` respectively. The behaviour of them both is identical for defining and slots and signals. 

The following PyQt5 and PySide2 examples are identical —

```python
my_custom_signal = pyqtSignal()  # PyQt5
my_custom_signal = Signal()  # PySide2

my_other_signal = pyqtSignal(int)  # PyQt5
my_other_signal = Signal(int)  # PySide2
```

Or for a slot —
```python
@pyqtslot
def my_custom_slot():
    pass

@Slot
def my_custom_slot():
    pass
```

If you want to ensure consistency across PyQt5 and PySide2 you can use the following import pattern for PyQt5 to use the `Signal` and `@Slot` style there too.

```python
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
```


You could of course do the reverse `from PySide2.QtCore import Signal as pyqtSignal, Slot as pyqtSlot` although that's a bit confusing.

## 文件管理（[QFileDialog](https://doc.qt.io/qtforpython/PySide2/QtWidgets/QFileDialog.html?highlight=qfiledialog#PySide2.QtWidgets.PySide2.QtWidgets.QFileDialog.setFileMode)）

![Inheritance diagram of PySide2.QtWidgets.QFileDialog](learn-GUI.assets/inheritance-3a3198aa2a543952963b7965bd4d71a35f510788.png)

[文件树](https://blog.csdn.net/qq_27061049/article/details/89641210)、

可以通过treeview和Dock实现：

```python
    def setDock():
        self.fileTree = QDockWidget()
        self.fileTree.setWindowTitle('Bookmarks')
        self._bookmark_widget = FileTreeWidget()
        self._bookmark_widget.open_bookmark.connect(self.load_url)
        self._bookmark_widget.open_bookmark_in_new_tab.connect(self.load_url_in_new_tab)
        self.fileTree.setWidget(self._bookmark_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.fileTree)
        
```


## Python 与 QML 通信
首先，对于每一个界面 (QML 文件)，我们都有一个与之对应 Python 文件 (除非该页面没有具体的业务逻辑，例如：`ui\SciHubEVAAbout.qml` 为关于页面，`ui\SciHubEVAMenuBar.qml` 为菜单栏)，以主页面 (`ui\SciHubEVA.qml` 和 `scihub_eva.py`) 为例，我们为每个界面创建一个类，同时该类集成自 Qt 的一个基类：

```python
class SciHubEVA(QObject):
    pass
```

Python 代码同界面交互的核心是通过 Qt 的 [**信号与槽**](http://doc.qt.io/qt-5/signalsandslots.html)，同样在 PyQt 中也是利用 [相同的机制](http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html)。简单的理解 PyQt 与 QML 的信号与槽，可以认为**信号**就是**函数的定义**，**槽**就是**函数的实现**。同时，信号和槽往往会位于不同的地方，例如：信号定义在 Python 中，则对应的槽会在 QML 中，反之亦然，当然这并不是一定的。两者通过 `connect()` 函数连接起来，当触发一个信号时，槽就会接受到信号传递的参数，并执行槽里面相应的逻辑。

## [动画](https://het.as.utexas.edu/HET/Software/PyQt/qeasingcurve.html)

```python

    def show_hide_menu(self,checked):
        print("显示和隐藏",checked)
        animation_group = QSequentialAnimationGroup(self)
        for idx,target in enumerate(self.animation_targets):
            animation = QPropertyAnimation(target,b"pos")

            animation.setStartValue(self.main_menu_btn.pos())
            animation.setEndValue(self.animation_targets_pos[idx])

            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.InOutBounce)
            animation_group.addAnimation(animation)

        if checked:
            animation_group.setDirection(QAbstractAnimation.Backward)
        else:
            animation_group.setDirection(QAbstractAnimation.Forward)

        animation_group.start(QAbstractAnimation.DeleteWhenStopped) #动画停止之后，给它删除

```

## 资源文件（qrc）
- [在PyQt中使用qrc-rcc资源系统](https://github.com/muziing/PySide6-Code-Tutorial/blob/main/07-Packaging-资源管理与打包/01-资源管理/01-在PyQt中使用qrc-rcc资源系统.md)
在 GUI 编程中，我们不可避免的会使用到各种各样的资源，例如：图片，音频，字体等等。Qt 中提供了一种[资源管理方案](http://doc.qt.io/qt-5/resources.html)，可以在不同场景下使用 (Python 和 QML 中均可)。`SciHubEVA.qrc` 定义了所有使用到的资源：

```xml
<RCC>
    <qresource prefix="/">
        <file>ui/SciHubEVA.qml</file>
        <file>ui/SciHubEVAMenuBar.qml</file>
        <file>ui/SciHubEVAAbout.qml</file>
        <file>ui/SciHubEVAPreferences.qml</file>
        <file>ui/SciHubEVAAddSciHubURL.qml</file>
        <file>images/about.png</file>
    </qresource>
</RCC>
```

在 QML 中使用示例如下：

```qml
Image {
    id: imageAboutLogo
    source: "qrc:/images/about.png"
}
```

在 Python 中使用示例如下：

```python
self._engine = QQmlApplicationEngine()
self._engine.load('qrc:/ui/SciHubEVA.qml')
```

使用 `qrc` 文件管理资源文件的一个好处就是不需要担心各种相对路径和绝对路径带来的找不到文件的错误，但同时一个缺点是当资源文件更新后，需要运行 `pyrcc5 SciHubEVA.qrc -o scihub_resources.py` 更新资源，同时还需要在主程序代码中引入生成的 Python 资源代码。

## [界面线程分离](https://www.cnblogs.com/zach0812/p/11426719.html)

写 GUI 应用的一个重要问题就是界面线程的分离，需要把耗时的业务逻辑摘出来，单独作为一个线程运行，这样才不会造成界面的“假死”情况。`scihub_api.py` 中的 `SciHubAPI` 作为下载文章的主类，下载过程相对耗时。因为其既需要 Qt 中的 `tr()` 函数，也需要线程，通过 Python 的多继承，`SciHubAPI` 类构造如下：

```python
class SciHubAPI(QObject, threading.Thread):
    pass
```

```python
import threading

from PyQt5.Qt import * #刚开始学习可以这样一下导入
import sys,time

rate = 0
class MyProcessBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test的学习")
        self.resize(300,30)
        self.set_ui()

    def set_ui(self):
        timer = QTimer(self)
        timer.start(100)
        timer.timeout.connect(self.timer_timeout_slot)

    def timer_timeout_slot(self):
        self.setValue(rate+1)

def create_ui_show():
    app =QApplication(sys.argv)
    processBar = MyProcessBar()
    processBar.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    thread1 = threading.Thread(target=create_ui_show)
    thread1.start()

    for i in range(100):
        time.sleep(0.05)
        rate = i
    if i == 99:
        print("下载完成")
```

```python
import multiprocessing

from PyQt5.Qt import * #刚开始学习可以这样一下导入
import sys,time

def create_ui_show(rate):
    app  = QApplication(sys.argv)
    progressBar = QProgressBar()

    timer = QTimer()
    def test():
        progressBar.setValue(rate.value+1)
        if rate.value == 99:
            sys.exit(0)
    timer.timeout.connect(test)
    timer.start(100)

    progressBar.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    rate = multiprocessing.Value("d",0)  #初始的rate.value = 0

    process1 = multiprocessing.Process(target=create_ui_show,args=(rate,))
    process1.start()

    for i in range(100):
        time.sleep(0.1)
        rate.value = i
```

# 开源项目分析

## [Modern_GUI_PyDracula_PySide6_or_PyQt6](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)
根据这个项目的文件和目录结构，以及一些常见的 Python 和 Qt 的项目构建流程，我们可以推测这个项目的构建过程可能如下：

1. **设计用户界面**：使用 Qt Designer 或其他 UI 设计工具创建 UI 设计，保存为 `.ui` 文件。在这个项目中，这个文件是 `main.ui`。
2. **转换 UI 文件**：使用 `pyside6-uic` 或 `pyuic6`（取决于你使用的是 PySide6 还是 PyQt6）将 `.ui` 文件转换为 Python 文件。在这个项目中，这个文件可能是 `ui_main.py`。
3. **编写代码**：在 `modules` 和 `widgets` 文件夹中编写 Python 代码，实现应用程序的逻辑和功能。这些代码使用了在步骤 2 中生成的 UI 类，以及其他的 Qt 类和模块。
4. **添加资源**：添加图像、图标和其他资源到项目中。这些资源可能被用于项目的用户界面。在这个项目中，这些资源被保存在 `images` 文件夹中。另外，`themes` 文件夹中的 `.qss` 文件是 Qt 样式表文件，用于设置应用程序的样式和主题。
5. **编写主程序**：在 `main.py` 文件中编写主程序，这个程序导入并使用了在步骤 3 中编写的模块，以及在步骤 2 中生成的 UI 类。主程序创建了一个 QApplication 实例和一个 QMainWindow 实例，并显示了主窗口。
6. **运行程序**：运行 `main.py` 文件，启动应用程序。

## QA
### 问题1：app_functions.py和main.py不在一个文件夹，为何语句 from main import * 可以导入main.py

> ChatGPT

在Python中，`from module import *` 语句会查找系统路径（sys.path）中的模块。`sys.path` 是一个列表，它包含了Python解释器查找模块的路径。当你运行一个Python脚本时，脚本的当前目录会自动添加到 `sys.path` 中。

如果 `main.py` 和 `app_functions.py` 不在同一个目录，`from main import *` 可能仍然能够正确工作，因为以下几个可能的原因：

1. 如果你是在项目的根目录下运行 `main.py` 文件，那么项目的根目录会被添加到 `sys.path`，因此 `main.py` 可以被找到。
2. 你的Python环境可能已经被配置为在其他的路径下查找模块。例如，你可能已经将项目的根目录或其他包含 `main.py` 的目录添加到了Python的环境变量 `PYTHONPATH` 中。
3. 你可能在运行脚本之前更改了当前目录，使得 `main.py` 所在的目录变成了当前目录。

然而，这种将脚本放在不同目录并直接导入的方式并不是一个好的做法，因为它使得代码的结构变得不清晰，也增加了维护难度。在大型项目中，通常会将代码组织成包和模块，并使用相对导入或绝对导入的方式来导入模块。在这个项目中，如果 `app_functions.py` 需要使用 `main.py` 中的代码，那么更好的方式可能是将共享的代码放在一个单独的模块中，然后在 `main.py` 和 `app_functions.py` 中都导入这个模块。

### 问题2：pyside6 串口数据实时显示

> ChatGPT

要实现在 PySide6 中实现串口数据的实时显示，你需要先安装 `pyserial` 库以便读取串口数据。然后，你可以使用 PySide6 的 `QTextEdit` 或 `QPlainTextEdit` 控件来显示数据。

由于此环境无法访问硬件接口，我无法在这里提供完全的示例代码，但是以下是一个基本的框架，你可以在你自己的环境中试试：
```python
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtCore import QTimer
import serial
import sys

class SerialReader:
    def __init__(self, port, baudrate):
        self.serial_port = serial.Serial(port, baudrate)

    def read(self):
        if self.serial_port.in_waiting > 0:
            return self.serial_port.read(self.serial_port.in_waiting).decode()
        else:
            return ''

class MainWindow(QMainWindow):
    def __init__(self, serial_reader):
        super().__init__()

        self.serial_reader = serial_reader
        self.text_edit = QTextEdit(self)

        self.setCentralWidget(self.text_edit)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second

    def update_data(self):
        data = self.serial_reader.read()
        self.text_edit.append(data)

def main():
    app = QApplication(sys.argv)

    serial_reader = SerialReader('COM3', 9600)  # Use your serial port and baudrate
    window = MainWindow(serial_reader)
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
```

在这个代码中，我们首先定义了一个 `SerialReader` 类，它包装了 `pyserial` 库的基本功能，用于读取串口数据。然后，我们创建了一个 `MainWindow` 类，它是一个包含 `QTextEdit` 控件的 `QMainWindow`。我们使用 `QTimer` 每秒更新一次 `QTextEdit` 的内容。

请注意，这个代码中的串口参数（'COM3', 9600）是示例值，你需要根据你的硬件设置进行修改。此外，你可能还需要根据你的需求调整定时器的频率（目前设为每秒更新一次）。



上述代码能用QtSerialPort代替pyserial实现吗

是的，你完全可以使用 Qt 的 QtSerialPort 模块来替代 pyserial。下面是一个使用 QtSerialPort 实现的例子：
```python
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtCore import QTimer
from PySide6.QtSerialPort import QSerialPort
import sys

class MainWindow(QMainWindow):
    def __init__(self, port_name, baud_rate):
        super().__init__()

        self.serial_port = QSerialPort()
        self.serial_port.setPortName(port_name)
        self.serial_port.setBaudRate(baud_rate)
        self.serial_port.open(QSerialPort.ReadWrite)

        self.text_edit = QTextEdit(self)

        self.setCentralWidget(self.text_edit)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second

    def update_data(self):
        if self.serial_port.canReadLine():
            data = self.serial_port.readLine().data().decode()
            self.text_edit.append(data)

def main():
    app = QApplication(sys.argv)

    window = MainWindow('COM3', QSerialPort.Baud9600)  # Use your serial port and baudrate
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
```

在这个代码中，我们创建了一个 `QSerialPort` 实例并设置了串口名称和波特率，然后我们每秒读取一次串口的数据并将其添加到 `QTextEdit` 控件中。

同样，代码中的串口参数（'COM3', QSerialPort.Baud9600）是示例值，你需要根据你的硬件设置进行修改。