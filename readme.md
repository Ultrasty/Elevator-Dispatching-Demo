# 电梯调度

###### 操作系统第一次作业

### 1851521 沈天宇



## 项目介绍

本项目已托管在GitHub上，项目地址https://github.com/Ultrasty/Elevator-Dispatching-Demo

### 1.背景

#### 基本任务

某一层楼20层，有五部互联的电梯。基于线程思想，编写一个电梯调度程序。

#### 功能描述

- [x] 电梯应有一些按键，如：数字键、关门键、开门键、上行键、下行键、报警键等；

- [x] 有数码显示器指示当前电梯状态；

- [x] 每层楼、每部电梯门口，有上行、下行按钮、数码显示。

#### 基本要求

- [x] 五部电梯相互联结，即当一个电梯按钮按下去时，其它电梯相应按钮同时点亮，表示也按下去了。

- [x] 电梯调度算法；

- [x] 所有电梯初始状态都在第一层；

- [x] 每个电梯没有相应请求情况下，则应该在原地保持不动；

- [x] 电梯调度算法自行设计。

### 2.开发

+ 使用`python`进行开发
+ `GUI`开发使用的图形库为`pyqt5`
+ `python`版本为`3.8.1`
+ 过程式编程，电梯的状态使用一组全局变量表示，未给每部电梯设计一个类，线程间通过共享的这组全局变量进行通信，通过维护这组变量实现电梯的调度
+ 运行：在根目录下运行如下命令

```bash
pip install pyqt5
python Elevator.py
```

+ 或者运行打包好的.exe文件

```bash
.\Elevator.exe
```



## 具体实现

过程式编程，电梯的状态使用一组全局变量表示，未给每部电梯设计一个类，线程间通过共享的这组全局变量进行通信，通过维护这组变量实现电梯的调度。



## 遇到的问题以及解决

程序在运行的时候有时候会崩溃，我怀疑是因为多线程读写冲突，于是让线程在读写要维护的全局变量的时候必须先获得一个锁。



## 运行演示

+ 初始状态

  

  ![初始状态](初始状态.png)



## 心得体会

​		此次项目作业是使用`python`语言编写的，因为代码简单可以节省不少时间用来界面布局。因为之前基本都是用` c++`语言，所以花了一定的时间来熟悉`python`以及`pyqt5`。经过多次调试运行来修正代码，对于一个小型`python`项目有了一个简单的了解，并且对特定环境下多线程编程方法更加熟悉了。

## 参考书籍

因开发`GUI`需要用到*PyQt5*,因此参考了《*PyQt5*快速开发与实战》

另外还参考了*PyQt5*中文教程https://github.com/maicss/PyQt5-Chinese-tutorial