# 前言-Python-Qt

## 不错的pyside开源项目
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
> [Qt for Python - Qt for Pythondoc.qt.io](https://link.zhihu.com/?target=https%3A//doc.qt.io/qtforpython/)[PyQt5 Reference Guidewww.riverbankcomputing.com![图标](https://pic1.zhimg.com/v2-2eb7f384cad652e57235db5f4b9acf6c_ipico.jpg)](https://link.zhihu.com/?target=https%3A//www.riverbankcomputing.com/static/Docs/PyQt5/)
> （从文档看我还是倾向用Qt for Python的）
> 

# 技术框架




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

## 资源文件

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
