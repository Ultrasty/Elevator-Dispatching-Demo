# -*- coding: utf-8 -*-
# @Time    : 2020/05/10
# @Author  : STY
# @Email   : 1455670697@qq.com
# @File    : Elevator.py
# @Software: PyCharm


import sys
import time
from functools import partial

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Example(QWidget):  # 主窗口

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置背景图片
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap("beijing.png")))
        # self.setPalette(palette)

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
                self.button.clicked.connect(partial(set_goal, inti + 1, intj))
                # self.button.clicked.connect(lambda: setgoal(inti+1,intj))# 为啥用lambda运行会出错啊...明明和partial一样的...
                intj = intj + 1
                self.button.setMaximumHeight(60)  # 按钮最大高度
                grid.addWidget(self.button, position[0] + 2, position[1] + inti * 3)

        for i in range(5):
            self.lcd = QLCDNumber()  # 数字显示
            # self.lcd.setStyleSheet("QLCDNumber{background-image: url(open.png)}")
            self.lcd.setObjectName("{0}".format(i + 1))
            grid.addWidget(self.lcd, 0, 3 * i, 2, 2)
            self.lab = QLabel(self)  # 这几个label是为了增加缝隙
            grid.addWidget(self.lab, 0, 3 * i + 2, 1, 1)
        for i in range(grid.rowCount()):
            grid.setRowMinimumHeight(i, 60)

        # 暂停按钮
        for i in range(5):
            self.button = QPushButton("暂停")
            self.button.setFont(QFont("Microsoft YaHei", 12))
            self.button.setObjectName("pause{0}".format(i + 1))
            self.button.setMinimumHeight(40)
            self.button.clicked.connect(partial(pause, i + 1))
            grid.addWidget(self.button, 12, 3 * i, 1, 2)

        # OPEN显示在下面的按钮上
        for i in range(5):
            self.button = QPushButton()
            self.button.setObjectName("open{0}".format(i + 1))
            self.button.setMinimumHeight(80)
            grid.addWidget(self.button, 13, 3 * i, 1, 2)

        # --------------------------------------下面是右边布局--------------------------------------#
        fori = 0
        for i in nameforallup:
            self.button = QPushButton(i)
            self.button.setFont(QFont("Microsoft YaHei"))
            self.button.setObjectName("up{0}".format(fori + 1))
            self.button.setMinimumHeight(42)
            self.button.clicked.connect(partial(set_global_goal_up, fori + 1))
            gridoutright.addWidget(self.button, 20 - fori, 0)
            fori = fori + 1

        fori = 0
        for i in nameforalldown:
            self.button = QPushButton(i)
            self.button.setFont(QFont("Microsoft YaHei"))
            self.button.setObjectName("down{0}".format(fori + 1))
            self.button.setMinimumHeight(42)
            self.button.clicked.connect(partial(set_global_goal_down, fori + 1))
            gridoutright.addWidget(self.button, 20 - fori, 1)
            fori = fori + 1

        # ----------------------------------------------------------------------------------------#
        self.move(10, 10)
        self.setWindowTitle('Elevator-Dispatching Copyright@2020 沈天宇')
        self.show()


class WorkThread(QThread):
    # 实例化一个信号对象
    trigger = pyqtSignal(int)

    def __init__(self, the_int):
        super(WorkThread, self).__init__()
        self.int = the_int
        self.trigger.connect(check)

    def run(self):
        while (1):


            if should_sleep[self.int - 1] == 1:
                ex.findChild(QPushButton, "open{0}".format(self.int)).setStyleSheet(
                    "QPushButton{background-image: url(open.png)}")
                time.sleep(2)
                ex.findChild(QPushButton, "open{0}".format(self.int)).setStyleSheet(
                    "QPushButton{}")

                should_sleep[self.int - 1] = 0
            if should_sleep[self.int - 1 + 5] == 1:
                ex.findChild(QPushButton, "open{0}".format(self.int)).setStyleSheet(
                    "QPushButton{background-image: url(open.png)}")

                time.sleep(2)
                ex.findChild(QPushButton, "open{0}".format(self.int)).setStyleSheet(
                    "QPushButton{}")

                should_sleep[self.int - 1 + 5] = 0
            self.trigger.emit(self.int)
            time.sleep(1)


def check(the_int):
    if pause[the_int - 1] == 1:
        # 改变电梯楼层

        if state[the_int - 1] == 0:
            pass
        else:
            if state[the_int - 1] == -1:
                floor[the_int - 1] = floor[the_int - 1] - 1
            else:
                floor[the_int - 1] = floor[the_int - 1] + 1
        ex.findChild(QLCDNumber, "{0}".format(the_int)).display(floor[the_int - 1])
        ex.findChild(QPushButton, "{0}+{1}".format(the_int, floor[the_int - 1])).setStyleSheet(
            "QPushButton{}")  # 去掉该层的标识

        # 从外部等候楼层中移除该层
        if state[the_int - 1] == -1:
            ex.findChild(QPushButton, "down{0}".format(floor[the_int - 1])).setStyleSheet(
                "QPushButton{}")  # 移除标识
        if state[the_int - 1] == 1:
            ex.findChild(QPushButton, "up{0}".format(floor[the_int - 1])).setStyleSheet(
                "QPushButton{}")  # 移除标识
        if state[the_int - 1] == 1:
            if (floor[the_int - 1] in elevator_goal[the_int - 1]) or (floor[the_int - 1] in people_up):
                should_sleep[the_int - 1] = 1

        if state[the_int - 1] == -1:
            if (floor[the_int - 1] in elevator_goal[the_int - 1]) or (floor[the_int - 1] in people_down):
                should_sleep[the_int - 1 + 5] = 1

        if state[the_int - 1] == 1:
            people_up.discard((floor[the_int - 1]))  # 移除楼层
        if state[the_int - 1] == -1:
            people_down.discard(floor[the_int - 1])  # 移除楼层
        elevator_goal[the_int - 1].discard(floor[the_int - 1])  # 从要达到的目标楼层中移除该层

        # ----------------------状态改变的算法---------------------- #

        if state[the_int - 1] == -1:  # 如果当前状态是向下
            if len(list(elevator_goal[the_int - 1])) == 0:
                state[the_int - 1] = 0
            if (len(list(elevator_goal[the_int - 1])) != 0) and (
                    min(list(elevator_goal[the_int - 1])) > floor[the_int - 1]):
                state[the_int - 1] = 1

        if state[the_int - 1] == 1:  # 如果当前状态是向上
            if len(list(elevator_goal[the_int - 1])) == 0:
                state[the_int - 1] = 0
            if (len(list(elevator_goal[the_int - 1])) != 0) and (
                    max(list(elevator_goal[the_int - 1])) < floor[the_int - 1]):
                state[the_int - 1] = -1

        if state[the_int - 1] == 0:  # 如果当前状态是静止
            if (len(list(elevator_goal[the_int - 1])) != 0) and (
                    max(list(elevator_goal[the_int - 1])) > floor[the_int - 1]):
                state[the_int - 1] = 1
            if (len(list(elevator_goal[the_int - 1])) != 0) and (
                    min(list(elevator_goal[the_int - 1])) < floor[the_int - 1]):
                state[the_int - 1] = -1

        # -----------------------显示电梯楼层----------------------- #
        ex.findChild(QLCDNumber, "{0}".format(the_int)).display(floor[the_int - 1])
        # ------------------------间隔的时间------------------------ #


def pause(elev):
    if pause[elev - 1] == 0:
        pause[elev - 1] = 1
        ex.findChild(QPushButton, "pause{0}".format(elev)).setText("暂停")
    else:
        pause[elev - 1] = 0
        ex.findChild(QPushButton, "pause{0}".format(elev)).setText("启动")


def set_goal(elev, flr):  # 设定目标楼层

    ex.findChild(QPushButton, "{0}+{1}".format(elev, flr)).setStyleSheet(
        "QPushButton{background-image: url(background.png)}")
    elevator_goal[elev - 1].add(flr)


def set_global_goal_up(flr):  # 设定楼道里上楼请求所在的楼层
    ex.findChild(QPushButton, "up{0}".format(flr)).setStyleSheet("QPushButton{background-image: url(background.png)}")
    people_up.add(flr)
    elevator_goal[
        [abs(floor[0] - flr), abs(floor[1] - flr), abs(floor[2] - flr), abs(floor[3] - flr), abs(floor[4] - flr)].index(
            min(abs(floor[0] - flr), abs(floor[1] - flr), abs(floor[2] - flr), abs(floor[3] - flr),
                abs(floor[4] - flr)))].add(flr)


def set_global_goal_down(flr):  # 设定楼道里下楼请求所在的楼层
    ex.findChild(QPushButton, "down{0}".format(flr)).setStyleSheet("QPushButton{background-image: url(background.png)}")
    people_down.add(flr)
    elevator_goal[
        [abs(floor[0] - flr), abs(floor[1] - flr), abs(floor[2] - flr), abs(floor[3] - flr), abs(floor[4] - flr)].index(
            min(abs(floor[0] - flr), abs(floor[1] - flr), abs(floor[2] - flr), abs(floor[3] - flr),
                abs(floor[4] - flr)))].add(flr)


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
    should_sleep = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 此数组表示电梯状态 0表示停止 1表示向上运行 -1表示向下运行
    state = []
    for i in range(5):
        state.append(0)

    # 指示该电梯是否暂停运行
    pause = []
    for i in range(5):
        pause.append(1)

    # 表示当前楼层
    floor = []
    for i in range(5):
        floor.append(1)

    # 表示楼道里的向上的请求
    people_up = set([])

    # 表示楼道里的向下的请求
    people_down = set([])

    # 5个锁

    # 五个线程对应五部电梯，每隔一定时间检查每部电梯的状态和elevator_goal数组，并作出相应的行动
    t1 = WorkThread(1)
    t2 = WorkThread(2)
    t3 = WorkThread(3)
    t4 = WorkThread(4)
    t5 = WorkThread(5)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    sys.exit(app.exec_())  # 应用程序主循环
