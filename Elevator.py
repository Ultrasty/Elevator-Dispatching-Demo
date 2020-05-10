import sys,threading,time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets



class Example(QWidget):#主窗口

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(0)
        self.setLayout(grid)
        names = [('%s'%i) for i in range(1,21)]
        positions = [(i,j) for j in range(2) for i in range(10)]

        nameforall1=[('▲%s'%i) for i in range(1,21)]
        nameforall2=[('▼%s'%i) for i in range(1,21)]

        for inti in range(5):
            for position, name in zip(positions, names):
                if name == '':
                    continue
                button = QPushButton(name)
                button.setFont(QFont("Microsoft YaHei", 12))
                button.setMaximumHeight(60)#按钮最大高度
                grid.addWidget(button, position[0]+2,position[1]+inti*3)


        for i in range(5):
            self.lcd = QLCDNumber(self)
            grid.addWidget(self.lcd,0,3*i,2,2)
            self.lab=QLabel(self)
            grid.addWidget(self.lab, 0, 3 * i+2, 1, 1)

        for i in range(grid.rowCount()):
            grid.setRowMinimumHeight(i, 60)

        self.move(300, 150)
        self.setWindowTitle('Elevator-Dispatching Copyright@2020 STY')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    t=threading.Thread()
    sys.exit(app.exec_())#应用程序主循环