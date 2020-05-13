########################################################
#                                                      #
#                   操作系统 电梯调度                 #
#                   作者：1851521 沈天宇
#                   版权所有 侵权必究
#
########################################################

import sys, threading, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial


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

        nameforallup = [('▲ %s' % i) for i in range(1, 21)]  # 走廊里的按钮，向上
        nameforalldown = [('▼ %s' % i) for i in range(1, 21)]  # 向下
        # --------------------------------------下面是左边布局--------------------------------------#
        for inti in range(5):
            intj = 1
            for position, name in zip(positions, names):
                if name == '':
                    continue
                self.button = QPushButton(name)
                self.button.setFont(QFont("Microsoft YaHei", 12))
                self.button.setObjectName("{0}+{1}".format(inti + 1, intj))
                self.button.clicked.connect(partial(set_goal, self.button))
                # self.button.clicked.connect(lambda: setgoal(inti+1,intj))# 为啥用lambda运行会出错啊...明明和partial一样的...
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
        for i in nameforallup:
            self.button = QPushButton(i)
            self.button.setFont(QFont("Microsoft YaHei"))
            self.button.setMinimumHeight(36)
            self.button.clicked.connect(partial(set_global_goal_up, self.button))
            gridoutright.addWidget(self.button, 20 - fori, 0)
            fori = fori + 1
        fori = 0
        for i in nameforalldown:
            self.button = QPushButton(i)
            self.button.setFont(QFont("Microsoft YaHei"))
            self.button.setMinimumHeight(36)
            self.button.clicked.connect(partial(set_global_goal_down, self.button))
            gridoutright.addWidget(self.button, 20 - fori, 1)
            fori = fori + 1

        # ----------------------------------------------------------------------------------------#
        self.move(300, 150)
        self.setWindowTitle('Elevator-Dispatching Copyright@2020 沈天宇')
        self.show()


# def changefloor():
#     while(1):
#         time.sleep(3)
#         ex.findChild(QPushButton, "1+7").setStyleSheet("QPushButton{}")


def set_goal(ob):
    ob.setStyleSheet("QPushButton{background-image: url(background.png)}")


def set_global_goal_up(ob):
    ob.setStyleSheet("QPushButton{background-image: url(background.png)}")


def set_global_goal_down(ob):
    ob.setStyleSheet("QPushButton{background-image: url(background.png)}")


def check_and_change_floor(int):
    pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    # 表示目标楼层
    elevator_goal1 = set([])
    elevator_goal2 = set([])
    elevator_goal3 = set([])
    elevator_goal4 = set([])
    elevator_goal5 = set([])
    elevator_goal = [elevator_goal1, elevator_goal2, elevator_goal3, elevator_goal4, elevator_goal5]

    # 此数组表示电梯状态 0表示停止 1表示向上运行 -1表示向下运行
    state = []
    for i in range(5):
        state.append(0)

    # 表示当前楼层
    floor = []
    for i in range(5):
        state.append(1)

    # 设置初始状态
    for i in range(5):
        ex.findChild(QLCDNumber, "{0}".format(i + 1)).display(1)

    # 五个线程对应五部电梯，每隔一定时间检查每部电梯的状态和elevator_goal数组，并作出相应的行动
    t1 = threading.Thread(target=check_and_change_floor(1))
    t2 = threading.Thread(target=check_and_change_floor(2))
    t3 = threading.Thread(target=check_and_change_floor(3))
    t4 = threading.Thread(target=check_and_change_floor(4))
    t5 = threading.Thread(target=check_and_change_floor(5))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    sys.exit(app.exec_())  # 应用程序主循环
