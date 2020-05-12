import sys, threading, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Example(QWidget):  # 主窗口

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        wlayout = QHBoxLayout()  # 总体布局：横向，其中嵌套了两个网格布局，emmmm 目前总体感觉还行，不想花时间美化了，先写业务逻辑
        gridoutright = QGridLayout()
        grid = QGridLayout()
        grid.setSpacing(0)
        gridoutright.setSpacing(0)
        gwg = QWidget()  # 准备部件
        rightwg = QWidget()
        gwg.setLayout(grid)  # 部件设置局部布局
        rightwg.setLayout(gridoutright)
        wlayout.addWidget(gwg)  # 部件加至全局布局
        wlayout.addWidget(rightwg)
        self.setLayout(wlayout)  # 窗体本体设置全局布局
        names = [('%s' % i) for i in range(1, 21)]  # 电梯按钮编号
        positions = [(i, j) for j in range(2) for i in range(10)]  # 位置

        nameforall1 = [('▲ %s' % i) for i in range(1, 21)]  # 走廊里的按钮，向上
        nameforall2 = [('▼ %s' % i) for i in range(1, 21)]  # 向下
        # --------------------------------------下面是左边布局--------------------------------------#
        for inti in range(5):
            intj = 1
            for position, name in zip(positions, names):
                if name == '':
                    continue
                self.button = QPushButton(name)
                self.button.setFont(QFont("Microsoft YaHei", 12))
                self.button.setObjectName("{0}+{1}".format(inti + 1, intj))
                intj = intj + 1
                self.button.setMaximumHeight(60)  # 按钮最大高度
                grid.addWidget(self.button, position[0] + 2, position[1] + inti * 3)
        for i in range(5):
            self.lcd = QLCDNumber()  # 数字显示
            self.lcd.setObjectName("{0}".format(i + 1))
            grid.addWidget(self.lcd, 0, 3 * i, 2, 2)
            self.lab = QLabel(self)  # 这几个label是为了增加缝隙
            grid.addWidget(self.lab, 0, 3 * i + 2, 1, 1)
        for i in range(grid.rowCount()):
            grid.setRowMinimumHeight(i, 60)

        # --------------------------------------下面是右边布局--------------------------------------#
        fori = 0
        for i in nameforall1:
            button = QPushButton(i)
            button.setFont(QFont("Microsoft YaHei"))
            button.setMinimumHeight(36)
            gridoutright.addWidget(button, 20 - fori, 0)
            fori = fori + 1
        fori = 0
        for i in nameforall2:
            button = QPushButton(i)
            button.setFont(QFont("Microsoft YaHei"))
            button.setMinimumHeight(36)
            gridoutright.addWidget(button, 20 - fori, 1)
            fori = fori + 1

        # ----------------------------------------------------------------------------------------#
        self.move(300, 150)
        self.setWindowTitle('Elevator-Dispatching Copyright@2020 沈天宇')
        self.show()


#def changefloor():
#    ex.findChild(QLCDNumber, "3").display(1)


#def changecolor():
#    ex.findChild(QPushButton, "5+17").setStyleSheet("background-color: white")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # 设2个全局变量 都是二维数组 第一位表示是第几部电梯 第二位表示这部电梯的哪几层有停泊请求
    # up表示想向上运行，down表示向下
    elevator_up = []
    elevator_down = []
    # 设置初始状态
    for i in range(5):
        ex.findChild(QLCDNumber, "{0}".format(i + 1)).display(1)
    # 线程
    # t1 = threading.Thread(target=changefloor)
    # t1.start()
    sys.exit(app.exec_())  # 应用程序主循环
