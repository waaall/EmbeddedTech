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


## 多进程与多线程


### python多进程
- [廖雪峰-多进程](https://liaoxuefeng.com/books/python/process-thread/process/index.html)
如果要启动大量的子进程，可以用进程池的方式批量创建子进程：

```python
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
```

执行结果如下：

```plain
Parent process 669.
Waiting for all subprocesses done...
Run task 0 (671)...
Run task 1 (672)...
Run task 2 (673)...
Run task 3 (674)...
Task 2 runs 0.14 seconds.
Run task 4 (673)...
Task 1 runs 0.27 seconds.
Task 3 runs 0.86 seconds.
Task 0 runs 1.41 seconds.
Task 4 runs 1.91 seconds.
All subprocesses done.
```
### python多线程只能单核？用它还有啥意义？
- [ 廖雪峰-多线程](https://liaoxuefeng.com/books/python/process-thread/thread/index.html)
- [python 多线程只能用一个核心](https://blog.51cto.com/u_12959/8988101)

  为什么python的多线程不能利用多核CPU，但是咱们在写代码的时候，多线程的确是在并发，而且还比单线程快。
原因：
因为GIL，python只有一个GIL，运行python时，就要拿到这个锁才能执行，在遇到！/O 操作时会释放这把锁。

#### 1. 避免'卡死'
和计算机最开始出现进程管理的原因一样：比如UI调用了一个计算的类方法，这时候我们看起来就整个都卡死，等他结束才能干其他的，如果你开一个线程处理它，那就回调用系统的线程管理（也有可能是自己写的）让每个线程运行一段时间就让给线程队列的其他线程。这样我就能在计算“过程中”干其他的事。
这好像看起来使得我的计算任务反而变慢了很多，不一定，看下文：
#### 2. 计算密集型 vs. IO密集型
  为什么python的多线程不能利用多核CPU，但是咱们在写代码的时候，多线程的确是在并发，而且还比单线程快。
原因：
因为GIL，python只有一个GIL，运行python时，就要拿到这个锁才能执行，在遇到I/O 操作时会释放这把锁。
如果是纯计算的程序，没有I/O操作，解释器会每隔100次操作就释放这把锁，让别的线程有机会 执行（这个次数可以来调整）同一时间只会有一个获得GIL线程在跑，其他线程都处于等待状态
1、如果是CPU密集型代码（循环、计算等），由于计算工作量多和大，计算很快就会达到100，然后触发GIL的释放与在竞争，多个线程来回切换损耗资源，
所以在多线程遇到CPU密集型代码时，单线程会比较快
2、如果是I0密集型代码（文件处理、网络爬虫），开启多线程实际上是并发（不是并行），I0操作会进行I0等待，线程A等待时，自动切换到线程B，这时候效率就高了。

### python异步I/O
- [廖雪峰-使用asyncio](https://liaoxuefeng.com/books/python/async-io/asyncio/index.html)

asyncio 本身并不能自动判断哪些代码是需要进行 I/O 操作的。它只能调度那些显式地通过 await 关键字标识出来的异步任务。因此，如果你的 image_handler 函数中没有 await 语句，即使存在实际的 I/O 操作（如文件读取、网络请求等），asyncio 也无法自动识别并将它们非阻塞地调度。
#### asyncio 依赖显式的 await
1. **await** **的作用**：
• await 是用来暂停当前协程的执行并等待一个可等待对象（如异步 I/O 操作、协程或 Future）完成。只有通过 await，asyncio 的事件循环才能在任务之间切换。

2. **没有** **await** **的异步函数行为**：
• 如果 image_handler 中没有 await，整个函数会同步执行，即便它是一个 async def 定义的函数，也会像普通的同步函数一样运行完毕而不会让出控制权。
• 这意味着，即使你使用 asyncio.gather() 调度多个 image_handler，它们实际上会顺序执行，而不是并发执行。

3. **不能自动识别同步 I/O**：
• asyncio 不能自动识别和管理那些没有 await 标识的同步 I/O 操作。像 Image.open() 或 file.read() 这种传统的同步 I/O 操作，asyncio 无法对其进行非阻塞处理。

#### 如何确保真正的异步 I/O
为了让 asyncio 正确处理 I/O 操作并实现异步执行，需要确保以下几点：

1. **使用支持异步的库**：
• 使用支持异步的 I/O 库，比如 aiohttp 进行异步网络请求，aiofiles 进行异步文件读写。这些库的 I/O 操作本身就是异步的，可以被 await，从而让 asyncio 正确调度。

2. **显式使用** **await** **语句**：
• 在 image_handler 中，任何需要异步执行的操作都必须通过 await 调用。没有 await，事件循环无法在这些操作期间切换到其他任务。

### ThreadPoolExecutor、QThread 和 threading.Thread
ThreadPoolExecutor、QThread 和 threading.Thread 是 Python 中用于多线程编程的不同工具，它们在使用场景、实现方式和功能上有一些重要的区别和各自的优缺点。以下是它们的详细比较：

**1. ThreadPoolExecutor**
• **简介**：ThreadPoolExecutor 是 Python 标准库 concurrent.futures 模块中的一个高级 API，用于创建和管理线程池。它简化了多线程的实现，适合需要重复执行相似任务的场景。
• **特点**：

• **线程池管理**：自动管理线程的创建、销毁以及任务的调度。
• **简单易用**：使用方便，通过提交任务来管理线程，无需手动创建和管理每个线程。
• **易于扩展**：支持任务的结果获取、超时、取消等高级功能。
• **适用于 I/O 密集型任务**：如文件读写、网络请求等。

• **使用场景**：
• 批量任务处理，如图像处理、网络请求、文件 I/O 等。
• 需要管理大量短时间任务时，通过线程池提高效率。

• **优点**：
• 简化多线程编程。
• 线程池复用，避免频繁创建销毁线程带来的开销。
• 提供 Future 对象用于检查任务状态、获取结果等。

• **缺点**：
• 不适用于需要高度自定义线程行为的场景。
• 无法方便地与 PyQt 的信号槽机制集成。

**2. QThread**
• **简介**：QThread 是 PyQt/PySide 中的线程类，专为与 Qt 框架集成的多线程任务设计，支持与 Qt 的信号和槽机制交互。

• **特点**：
• **信号槽机制**：QThread 与 Qt 的信号槽系统无缝集成，适合 GUI 应用中使用。
• **事件循环**：可以在 QThread 中运行事件循环，适合需要处理异步事件的场景。
• **Qt 集成**：与 PyQt/PySide GUI 完美结合，方便更新界面。

• **使用场景**：
• 需要在 Qt 应用中运行后台任务，同时更新 GUI 的场景。
• 在 GUI 中处理长时间任务而不阻塞主线程。

• **优点**：
• 与 PyQt/PySide 的 GUI 组件集成良好，支持异步信号与槽的连接。
• 适用于 GUI 应用，处理后台任务并且更新界面。

• **缺点**：
• 依赖于 PyQt/PySide，不适用于独立的多线程需求。
• 使用相对复杂，尤其在管理线程生命周期和事件时。

**3. threading.Thread**
• **简介**：threading.Thread 是 Python 标准库中的低级线程类，提供了直接的多线程控制能力，可以完全自定义线程的行为。

• **特点**：
• **低级控制**：允许创建和管理独立的线程，提供高度自定义能力。
• **共享全局变量**：多个线程可以共享全局变量和资源。
• **直接控制**：可以控制线程的启动、停止和退出。

• **使用场景**：
• 需要高度自定义的线程行为。
• 适合简单的并发任务，或在非 GUI 程序中使用。

• **优点**：
• 高度灵活，能够完全控制线程的行为。
• 适用于各种不依赖于特定框架的多线程应用。

• **缺点**：
• 需要手动管理线程的生命周期，增加了编程复杂度。
• 无法自动管理线程池，需要自己控制线程的数量和调度。

**总结与对比**
• **ThreadPoolExecutor** 适合需要管理大量相似任务的场景，提供了简单的线程池管理和任务调度。
• **QThread** 是与 Qt 框架紧密集成的线程类，适用于 GUI 应用，能够方便地处理后台任务和界面更新。
• **threading.Thread** 提供了最大程度的控制，适合需要高度定制化的多线程任务，但需要手动管理线程的各个方面。

选择哪个工具取决于应用场景和具体需求，如果是与 PyQt 的 GUI 集成，使用 QThread 是最佳选择；如果只是需要简单的线程池管理，ThreadPoolExecutor 更为方便；而 threading.Thread 适合那些需要完全控制线程的场景。

### [界面线程分离](https://www.cnblogs.com/zach0812/p/11426719.html)
#### 使用Qthread单独

#### 使用threading
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


## 传递引用变量的危险
**可变对象作为默认参数的陷阱**：在 Python 中，默认参数是函数对象的属性，会在函数定义时被评估一次。因此，如果你将一个可变对象（如列表、字典等）作为默认参数，它会在所有实例之间共享。如果在某个实例中修改了这个列表，会影响所有其他实例。这是一个常见的陷阱。
```python
class SplitColors:
    def __init__(self, colors=['R', 'G', 'B']):
        self.colors = colors

a = SplitColors()
b = SplitColors()

a.colors.append('X')
print(b.colors)  # 输出 ['R', 'G', 'B', 'X']，b.colors 也受到了影响
```

## 控件为什么要传递self进去

在 PySide 中，`QPlainTextEdit` 控件的构造函数可以接受一个父级控件作为参数。`self` 通常指的是当前的主窗口或父级窗口。在大多数情况下，将 `self` 作为参数传递给 `QPlainTextEdit` 的构造函数是为了设置它的父级控件，这样做有以下几个好处：

### 1. 控制控件的生命周期
当你将 `self` 传递给 `QPlainTextEdit` 时，`QPlainTextEdit` 控件的生命周期会与它的父控件（通常是主窗口或另一个容器控件）绑定在一起。当父控件被销毁时，子控件也会自动销毁，无需手动管理子控件的内存。

### 2. 层级管理
通过指定父控件，可以确保控件在窗口的层级结构中正确显示。例如，如果你在主窗口中创建多个控件，并且将它们的父控件设置为主窗口（`self`），这些控件将按照你在布局中指定的方式显示，并且层级结构清晰。

### 3. 事件传播
在 Qt 的信号与槽机制中，事件可以在父子控件之间传播。如果控件有父级，事件会首先传递给子控件，然后再传递给父控件。这有助于统一处理某些事件，如按键或鼠标事件。

### 4. 确保控件显示在父窗口中
如果不传递 `self` 或其他父级控件，那么这个控件会成为一个独立的窗口（顶层窗口），而不是主窗口的一部分。在大多数 GUI 应用中，控件通常是嵌入在窗口中的一部分，而不是独立的窗口，因此需要指定父级控件。

### 示例代码

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPlainTextEdit, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # 设置主窗口布局
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 创建 QPlainTextEdit 控件，并将主窗口 self 作为其父级控件
        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setReadOnly(True)  # 设置为只读，避免用户直接修改内容
        self.layout.addWidget(self.text_edit)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()
```

### 解释：

- **`self` 作为父控件**：在这个例子中，`QPlainTextEdit(self)` 表示 `QPlainTextEdit` 控件的父级是 `MainWindow`，因此这个控件将嵌入在 `MainWindow` 中，而不是独立存在。

- **生命周期管理**：当 `MainWindow` 被销毁时，`QPlainTextEdit` 控件也会被自动销毁，确保不会有悬空指针或内存泄漏。

### 总结

将 `self` 传递给控件的构造函数是为了确保该控件与其父窗口或容器控件正确关联，确保它在 UI 层级结构中正确显示，并且简化内存和事件管理。这是 PySide 和 Qt 中常见的设计模式，能使得控件的行为更加直观和易于管理。

## 打包
pyinstaller用户打包python程序

```python
import subprocess
import sys

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def build_executable():
    # 检测操作系统
    current_platform = platform.system()

    if current_platform == "Windows":
        # Windows 平台的 PyInstaller 命令
        subprocess.check_call([sys.executable, "-m", "PyInstaller",
                               "--onedir",  # 生成一个文件夹,内部包含所有运行所需文件
                               "--windowed",
                               "--collect-submodules=pydicom", # 确保 pydicom 所需模块被包含
                               "--add-data", "libs/openh264-1.8.0-win64.dll;libs",  # dll添加到 libs 文件夹
                               "--add-data", "libs/openh264-1.8.0-win64.dll;.",  # dll添加到 exe 同一目录
                               "--name=Branden_RD_Tool",
                               "main.py"])
    elif current_platform == "Darwin":
        # macOS 平台的 PyInstaller 命令
        subprocess.check_call([sys.executable, "-m", "PyInstaller",
                               "--onefile",  # 生成一个单独的可执行文件
                               "--windowed",
                               "--collect-submodules=pydicom", # 确保 pydicom 所需模块被包含
                               "--name=Branden_RD_Tool",
                               "main.py"])
    else:
        try:
            subprocess.check_call([sys.executable, "-m", "PyInstaller",
                                   "--onefile",  # 生成一个单独的可执行文件
                                   "--windowed",
                                   "--icon=/resources/branden.ico",  # 图标路径
                                   "--add-data", "/resources/branden.ico:./",  # 添加数据
                                   "--hidden-import=pydicom",  # 确保 pydicom 模块被包含
                                   "--collect-submodules=pydicom",
                                   "--name=Branden_RD_Tool",
                                   "main.py"])
        raise Exception("Unsupported operating system")


if __name__ == "__main__":
    install_requirements()
    build_executable()
```
### os.name和platform.system
os.name 和 platform.system() 都可以用来获取操作系统的信息，但它们提供的信息和用途有所不同：
**os.name**
• **返回值**: os.name 返回的是一个简单的字符串，用来标识操作系统的类型：
• 'posix'：表示类 Unix 系统，如 Linux 和 macOS。
• 'nt'：表示 Windows 系统。
• 'java'：表示在 Java 平台上运行。
• **用途**: os.name 主要用于判断操作系统的类型，以决定执行特定的操作。例如，某些操作系统可能需要不同的路径分隔符或其他特定处理。

**platform.system()**
• **返回值**: platform.system() 返回的是一个字符串，表示操作系统的名称：
• 'Linux'：表示 Linux 系统。
• 'Darwin'：表示 macOS 系统。
• 'Windows'：表示 Windows 系统。
• 'Java'：表示在 Java 平台上运行。
• **用途**: platform.system() 提供了更详细的信息，通常用于需要操作系统名称的情况。例如，某些库或工具可能需要知道具体的操作系统名称以便进行更精确的处理。

**选择使用场景**
• **使用** **os.name**: 如果你只需要区分类 Unix 系统（如 Linux 和 macOS）和 Windows 系统，可以使用 os.name。它提供的信息较少，但足以区分主要的操作系统类别。
• **使用** **platform.system()**: 如果你需要具体的操作系统名称来进行更精细的操作（例如，执行特定于操作系统的命令或配置），platform.system() 提供了更详细的信息。

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

### 问题3  嵌套循环I/O的堵塞优化
我想要在函数self.selected_dirs_handler中循环处理多个其中的self._data_dir_handler，在函数self._data_dir_handler中循环处理多个其中的data_handler，还要在data_handler中循环处理多个其中的image_handler，其中每个image_handler都进行几次I/O操作，这种情况如何优化I/O延迟？

多线程或者异步I/O，但是异步I/O需要对应的I/O操作函数都要支持（一般都是不支持的）
所以简单来讲就是多线程设置更简单一些，但是异步I/O开销更小。具体还要看上文中的文档。

### 问题4 检查文件名后缀
`os.path.splitext(f)[1].lower() in self.suffixs`和
`any(f.endswith(suffix) for suffix in self.suffixs)`
这两句有什么区别?
这两句代码都用于检查文件的扩展名是否在指定的后缀列表中，但它们的实现方式和适用场景略有不同。以下是两者的区别和适用场景：

1. **`os.path.splitext(f)[1].lower() in self.suffixs`**：
   ```python
   # 使用 splitext 分离文件名和后缀，并检查后缀是否在指定的列表中
   result = os.path.splitext(f)[1].lower() in self.suffixs
   ```
   **实现方式**：
   - `os.path.splitext(f)[1]`：将文件名 `f` 分割为主文件名和扩展名，返回扩展名部分。
   - `.lower()`：将扩展名转换为小写，确保比较不区分大小写。
   - `in self.suffixs`：检查扩展名是否在指定的 `self.suffixs` 列表中。
   **适用场景**：
   - 适合用来匹配明确的、标准化的扩展名（例如 `.jpg`, `.png`, `.dcm`）。
   - 不适用于检查复杂的后缀模式（例如多个后缀或不标准的文件名）。
   **优点**：
   - 简单直接，清晰明了，适合精确匹配标准文件扩展名。
   - 处理 `.lower()` 保证了不区分大小写的匹配。
   **缺点**：
   - 仅能匹配文件的扩展名，不能匹配更复杂的模式。

2. **`any(f.endswith(suffix) for suffix in self.suffixs)`**：
   ```python
   # 使用 endswith 逐个检查文件名是否以指定的后缀结尾
   result = any(f.endswith(suffix) for suffix in self.suffixs)
   ```
   **实现方式**：
   - `f.endswith(suffix)`: 检查文件名 `f` 是否以某个 `suffix` 结尾。
   - `any(...)`：如果 `f` 以列表中的任意一个后缀结尾，则返回 `True`。
   **适用场景**：
   - 适合匹配各种复杂的文件名结尾模式，可以包括多种后缀、无扩展名或非标准的文件命名方式。
   - 允许匹配更灵活的文件名，如包含多个点的文件名（例如 `.tar.gz`、没有扩展名的文件等）。
   **优点**：
   - 更灵活，能够匹配复杂文件名和非标准扩展名。
   - 可以处理文件名中多个后缀或特殊格式的文件（如 `backup.tar.gz`）。
   **缺点**：
   - 需要显式地列出所有可能的后缀，容易出错，特别是当后缀种类较多时。

- **`os.path.splitext()` 更精确和清晰**，适合标准化的扩展名检查。它分割文件名并直接检查扩展名部分，适合于比较明确、常规的文件格式。
- **`any(f.endswith())` 更灵活和宽松**，适合处理各种复杂情况，包括非标准扩展名、多个后缀组合、或无扩展名的文件。
**使用建议**：
- 当需要精确匹配文件扩展名时，使用 `os.path.splitext()`。
- 当需要更广泛和灵活的匹配时，使用 `any(f.endswith())`。

