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
        wlayout = QHBoxLayout()  # 总体布局：横向
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
##############################################################################下面是左边布局
        for inti in range(5):
            for position, name in zip(positions, names):
                if name == '':
                    continue
                button = QPushButton(name)
                button.setFont(QFont("Microsoft YaHei", 12))
                button.setMaximumHeight(60)  # 按钮最大高度
                grid.addWidget(button, position[0] + 2, position[1] + inti * 3)
        for i in range(5):
            self.lcd = QLCDNumber(self)  # 数字显示
            grid.addWidget(self.lcd, 0, 3 * i, 2, 2)
            self.lab = QLabel(self)  # 这几个label是为了增加缝隙
            grid.addWidget(self.lab, 0, 3 * i + 2, 1, 1)
        for i in range(grid.rowCount()):
            grid.setRowMinimumHeight(i, 60)

##############################################################################下面是右边布局
        fori=0
        for i in nameforall1:
            button=QPushButton(i)
            button.setFont(QFont("Microsoft YaHei"))
            button.setMinimumHeight(36)
            gridoutright.addWidget(button,fori,0)
            fori=fori+1
        fori=0
        for i in nameforall2:
            button=QPushButton(i)
            button.setFont(QFont("Microsoft YaHei"))
            button.setMinimumHeight(36)
            gridoutright.addWidget(button,fori,1)
            fori=fori+1
##############################################################################
        self.move(300, 150)
        self.setWindowTitle('Elevator-Dispatching Copyright@2020 沈天宇')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    t = threading.Thread()
    sys.exit(app.exec_())  # 应用程序主循环
