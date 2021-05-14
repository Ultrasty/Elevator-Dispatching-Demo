

###### 操作系统第一次作业

<p align="left">
  <a href="https://circleci.com/gh/vuejs/vue/tree/dev"><img src="https://img.shields.io/circleci/project/github/vuejs/vue/dev.svg?sanitize=true" alt="Build Status"></a>
</p>


## 项目介绍

本项目已托管在GitHub上，项目地址https://github.com/Ultrasty/Elevator-Dispatching-Demo

导出的PDF格式代码缩进有点问题，可能还是在`GitHub`上看更加清楚

~~**程序经过调试，除了偶尔会闪退之外没有重大`bug` ！ **闪退可能是因为没用`QThread`而使用了`python`标准库自带的`threading`的原因，因为时间问题没有换过来。~~

- [x] 时隔一年，我回来把会闪退的毛病给改了，现在程序不会闪退。

bug产生的原因是跨线程操作UI，解决办法是利用pyqt5的emit

**相同的代码，在`linux`上也进行了测试，暂未发现闪退的现象！**

### 1.背景

#### 基本任务

某一层楼20层，有五部互联的电梯。基于线程思想，编写一个电梯调度程序。

#### 功能描述

- [x] 电梯应有一些按键，如：数字键、关门键、开门键、上行键、下行键、报警键等；

- [x] 有数码显示器指示当前电梯状态；

- [x] 每层楼、每部电梯门口，有上行、下行按钮、数码显示。

### 2.开发

+ 使用`python`进行开发
+ `GUI`开发使用的图形库为`pyqt5`
+ `python`版本为`3.8.1`
+ 过程式编程，电梯的状态使用一组全局变量表示，未给每部电梯设计一个类，线程间通过共享的这组全局变量进行通信，通过维护这组变量实现电梯的调度
+ 运行：在根目录下运行如下命令（安装PyQt5和运行程序）

```bash
pip install pyqt5
python Elevator.py
```

+ 或者运行打包好的.exe文件

```bash
.\Elevator.exe
```



## 具体算法

过程式编程，电梯的状态使用一组全局变量`elevator_goal`、`state`、`pause`、`floor`表示，线程间通过共享的这组全局变量进行通信，通过维护这组变量实现电梯的调度，使用一个锁`lock`保证读写不冲突。

```python
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
    lock = []
    for i in range(5):
        lock.append(threading.Lock())
```

当按下内部的按钮时，相应楼层会被添加至目标楼层

```python
def set_goal(elev, flr):  # 根据电梯内的按钮设定目标楼层
    lock[elev - 1].acquire()  # 获得锁
    ex.findChild(QPushButton, "{0}+{1}".format(elev, flr)).setStyleSheet(
        "QPushButton{background-image: url(background.png)}")
    elevator_goal[elev - 1].add(flr)
    lock[elev - 1].release()  # 释放锁
```

当按下外部的按钮时，该楼层会被设为某一部电梯的任务楼层，该电梯即为距离该楼层最近的一部电梯。

```python
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
```

上面两段代码是一样的，外部按钮的上楼和下楼区别在于，比如当外部按钮的▲10和▼10都被按下，而有一部电梯的升降路线为9->10->11则外部按钮的▲10会被清除而▼10会继续保持。此算法在函数`check_and_change_floor`中。

```python
    ...
    # 从外部等候楼层中移除该层
    if state[int - 1] == -1:
        ex.findChild(QPushButton, "down{0}".format(floor[int - 1])).setStyleSheet(
            "QPushButton{}")  # 移除标识
    if state[int - 1] == 1:
        ex.findChild(QPushButton, "up{0}".format(floor[int - 1])).setStyleSheet(
            "QPushButton{}")  # 移除标识
    ...
 
    ...
    if state[int - 1] == 1:
        people_up.discard((floor[int - 1]))  # 移除楼层
    if state[int - 1] == -1:
        people_down.discard(floor[int - 1])  # 移除楼层
    ...
```

五个线程每秒执行一次`check_and_change_floor`，进行更改当前楼层的操作，主要的算法也包含其中。

具体流程为先根据状态（上行、静止、下行）改变当前所在楼层，根据改变后的楼层从任务列表里去除相应楼层并且熄灭相应的按钮，再根据任务列表和当前所在的楼层改变电梯的状态。然后在睡眠1s之后，继续重复此流程。为每个电梯都安排一个这样的线程。

```python
def check_and_change_floor(int):
    while (1):

        if pause[int - 1] == 1:
            # 改变电梯楼层
            lock[int - 1].acquire()  # 加锁
            if state[int - 1] == 0:
                pass
            else:
                if state[int - 1] == -1:
                    floor[int - 1] = floor[int - 1] - 1
                else:
                    floor[int - 1] = floor[int - 1] + 1
            ex.findChild(QLCDNumber, "{0}".format(int)).display(floor[int - 1])
            ex.findChild(QPushButton, "{0}+{1}".format(int, floor[int - 1])).setStyleSheet(
                "QPushButton{}")  # 去掉该层的标识

            # 从外部等候楼层中移除该层
            if state[int - 1] == -1:
                ex.findChild(QPushButton, "down{0}".format(floor[int - 1])).setStyleSheet(
                    "QPushButton{}")  # 移除标识
            if state[int - 1] == 1:
                ex.findChild(QPushButton, "up{0}".format(floor[int - 1])).setStyleSheet(
                    "QPushButton{}")  # 移除标识
            if state[int - 1] == 1:
                if (floor[int - 1] in elevator_goal[int - 1]) or (floor[int - 1] in people_up):
                    lock[int - 1].release()
                    ex.findChild(QPushButton, "open{0}".format(int)).setStyleSheet(
                        "QPushButton{background-image: url(open.png)}")
                    time.sleep(2)
                    ex.findChild(QPushButton, "open{0}".format(int)).setStyleSheet(
                        "QPushButton{}")
                    lock[int - 1].acquire()

            if state[int - 1] == -1:
                if (floor[int - 1] in elevator_goal[int - 1]) or (floor[int - 1] in people_down):
                    lock[int - 1].release()
                    ex.findChild(QPushButton, "open{0}".format(int)).setStyleSheet(
                        "QPushButton{background-image: url(open.png)}")
                    time.sleep(2)
                    ex.findChild(QPushButton, "open{0}".format(int)).setStyleSheet(
                        "QPushButton{}")
                    lock[int - 1].acquire()

            if state[int - 1] == 1:
                people_up.discard((floor[int - 1]))  # 移除楼层
            if state[int - 1] == -1:
                people_down.discard(floor[int - 1])  # 移除楼层
            elevator_goal[int - 1].discard(floor[int - 1])  # 从要达到的目标楼层中移除该层

            # ----------------------状态改变的算法---------------------- #

            if state[int - 1] == -1:  # 如果当前状态是向下
                if len(list(elevator_goal[int - 1])) == 0:
                    state[int - 1] = 0
                if (len(list(elevator_goal[int - 1])) != 0) and (
                        min(list(elevator_goal[int - 1])) > floor[int - 1]):
                    state[int - 1] = 1

            if state[int - 1] == 1:  # 如果当前状态是向上
                if len(list(elevator_goal[int - 1])) == 0:
                    state[int - 1] = 0
                if (len(list(elevator_goal[int - 1])) != 0) and (
                        max(list(elevator_goal[int - 1])) < floor[int - 1]):
                    state[int - 1] = -1

            if state[int - 1] == 0:  # 如果当前状态是静止
                if (len(list(elevator_goal[int - 1])) != 0) and (
                        max(list(elevator_goal[int - 1])) > floor[int - 1]):
                    state[int - 1] = 1
                if (len(list(elevator_goal[int - 1])) != 0) and (
                        min(list(elevator_goal[int - 1])) < floor[int - 1]):
                    state[int - 1] = -1

            # -----------------------显示电梯楼层----------------------- #
            ex.findChild(QLCDNumber, "{0}".format(int)).display(floor[int - 1])
            # ------------------------间隔的时间------------------------ #
            lock[int - 1].release()  # 释放锁
        time.sleep(1)
```



## 其他功能

#### 暂停

通过变量pause指示某部电梯是否暂停，若第`i`部电梯的pause值为0，则表示暂停运行

通过线程的if语句检查该变量，如果值为零，则什么都不做，然后`time.sleep(1)`

```python
def check_and_change_floor(int):
    while (1):
        if pause[int - 1] == 1:
        # 做事
```



#### OPEN

在电梯到达某一目标楼层时，显示OPEN，持续2s，该状态电梯所在楼层保持不变

通过`sleep()`来使线程进入睡眠，并且在进入睡眠前释放掉锁。

```python
            if state[int - 1] == 1:
                if (floor[int - 1] in elevator_goal[int - 1]) or (floor[int - 1] in people_up):
                    lock[int - 1].release()
                    ex.findChild(QPushButton, "open{0}".format(int)).setStyleSheet(
                        "QPushButton{background-image: url(open.png)}")
                    time.sleep(2)
                    ex.findChild(QPushButton, "open{0}".format(int)).setStyleSheet(
                        "QPushButton{}")
                    lock[int - 1].acquire()

            if state[int - 1] == -1:
                if (floor[int - 1] in elevator_goal[int - 1]) or (floor[int - 1] in people_down):
                    lock[int - 1].release()
                    ex.findChild(QPushButton, "open{0}".format(int)).setStyleSheet(
                        "QPushButton{background-image: url(open.png)}")
                    time.sleep(2)
                    ex.findChild(QPushButton, "open{0}".format(int)).setStyleSheet(
                        "QPushButton{}")
                    lock[int - 1].acquire()
```



## 遇到的问题

程序在运行的时候有时候会崩溃，怀疑是因为多个线程同时读写一个变量导致的，于是让线程在读写要维护的全局变量的时候必须先获得一个锁，以进行线程间的同步。

```python
# 设定5个锁
    lock=[]
    for i in range(5):
        lock.append(threading.Lock())
```
需要读写系统要维护的变量时，必须先获得锁，读写完成后再释放锁

比如：（电梯每`1s`执行一次改变楼层的操作）

```python
def check_and_change_floor(int):
    while (1):
        # 改变电梯楼层
        lock[int-1].acquire() # 获得锁
        ...
        
        ...
        lock[int-1].release() # 释放锁
        time.sleep(1)
```
以及：（按钮按下时设定目标楼层）
```python
def set_goal(elev, flr):  # 设定目标楼层
    lock[elev-1].acquire() # 获得锁
    ...
    
    ...
    lock[elev-1].release() # 释放锁
```

但是后来这个问题又出现了，百度谷歌退出时的错误代码也没能找到答案，仔细的想了一下，可能是因为`python`标准库自带的threading和pyqt5不能很好的协作，因此每次运行都会出现一些随机性的问题，而`pyqt5`提供了一个`QThread`（`PyQt5.QtCore.QThread`）可以提供多线程编程功能，在`python`自带多线程库的前提下，`pyqt5`还要有自己的多线程方法，可能就是为了更好的进行同步吧，但是由于时间原因，所以没有将`threading`换成`QThread`。



## 运行演示

如果下面的图片显示不出来，买个代理吧。


+ 初始状态


![初始状态](https://img2020.cnblogs.com/blog/1997201/202005/1997201-20200516170358778-569006344.png)


+ 运行起来

![初始状态](https://img2020.cnblogs.com/blog/1997201/202005/1997201-20200516170410678-1164541146.png)

![初始状态](https://img2020.cnblogs.com/blog/1997201/202005/1997201-20200516170419608-534490734.png)



在`linux`上演示

![linux](https://img2020.cnblogs.com/blog/1997201/202005/1997201-20200516170340108-310058245.png)

更多的程序运行时详细信息可见我的录屏demo.mp4



## 心得体会

​		此次项目作业是使用`python`语言编写的，因为代码简单可以节省不少时间用来界面布局。因为之前基本都是用` c++`语言，所以花了一定的时间来熟悉`python`以及`pyqt5`。经过多次调试运行来修正代码，对于一个小型`python`项目有了一个简单的了解，并且对特定环境下多线程编程方法更加熟悉了。



## 参考书籍


因开发`GUI`需要用到*PyQt5*,因此参考了《*PyQt5*快速开发与实战》

另外还参考了*PyQt5*中文教程https://github.com/maicss/PyQt5-Chinese-tutorial



## 赞助


如果你觉得本文对你有帮助，欢迎支持一下作者，一分钱也是可以滴。

ETH 以太币：0xa91339Bba7AfE768a0001928DDB97A008B8bb125

![](https://user-images.githubusercontent.com/51046846/117927941-7606f600-b32d-11eb-97e0-41dcccbe3388.png)



