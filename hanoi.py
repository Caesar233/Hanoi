# -*- coding: utf-8 -*-
import sys
import re
import time
from disk import Disk
from stack import Stack
from PyQt5.QtWidgets import (QApplication, QAction, QWidget, QHBoxLayout, QLabel, QFrame, QTableWidget, QInputDialog,
    QMainWindow, QTableWidgetItem, QPushButton, QVBoxLayout, qApp, QScrollBar, QScrollArea, QLineEdit, QMessageBox)
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QTimer,  QObject, pyqtSignal, QRegExp, QRect, QCoreApplication

class Main(QMainWindow):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.initTower()
        self.initUI()

    def initTower(self):
        self.t1 = Stack(self.n)
        self.t2 = Stack(self.n)
        self.t3 = Stack(self.n)
        self.disks = []
        for i in range(1, self.n+1):
            self.disks.append(Disk(self.n - i+1, 1))
            self.t1.push(self.disks[i-1])
            print(self.disks[i-1].num)

    def initUI(self):
        self.setGeometry(60, 100, 1800, 550)
        self.setWindowTitle("Hanoi")
        self.show()
        self.showDialog()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawHanoi(qp)
        qp.end()

    def drawHanoi(self, qp):
        black = QColor(0, 0, 0)
        qp.setPen(black)
        #qp.setBrush(Qt.white)

        # qp.setBrush(brush)
        # 底盘
        qp.drawRect(60, 510, 520, 10)
        qp.drawRect(640, 510, 520, 10)
        qp.drawRect(1220, 510, 520, 10)
        # 柱子
        qp.drawRect(315, 120, 10, 390)
        qp.drawRect(895, 120, 10, 390)
        qp.drawRect(1475, 120, 10, 390)

        width = int((520-50)/self.n) #宽度
        height = int(384/self.n) #高度

        for disk in self.disks:
            i = disk.num-1
            if disk.current == 1:
                j = self.t1.location(disk) # 获得disk在栈中的位置
                qp.drawRect(320 - i * width / 2 - 20, 510 - (j+1) * height, width * i + 40, height)
            elif disk.current == 2:
                j = self.t2.location(disk)  # 获得disk在栈中的位置
                qp.drawRect(900 - i * width / 2 - 20, 510 - (j+1) * height, width * i + 40, height)
            elif disk.current == 3:
                j = self.t3.location(disk)  # 获得disk在栈中的位置
                qp.drawRect(1480 - i * width / 2 - 20, 510 - (j+1) * height, width * i + 40, height)

        # for i in range(self.n):
        #     #初始化盘子
        #     qp.drawRect(320-i*width/2-20, 510-(self.n-i)*height, width*i+40, height)

    def moveOneDisk(self, num, start, end):

        self.disks[self.n - num].current = end
        if start == 1:
            self.t1.pop()
            if end == 2:
                self.t2.push(self.disks[self.n - num])
                print("Move the %dth disks from %d to %d" % (num, start, end))
            elif end == 3:
                self.t3.push(self.disks[self.n - num])
                print("Move the %dth disks from %d to %d" % (num, start, end))
        elif start == 2:
            self.t2.pop()
            if end == 1:
                self.t1.push(self.disks[self.n - num])
                print("Move the %dth disks from %d to %d" % (num, start, end))
            elif end == 3:
                self.t3.push(self.disks[self.n - num])
                print("Move the %dth disks from %d to %d" % (num, start, end))
        elif start == 3:
            self.t3.pop()
            if end == 1:
                self.t1.push(self.disks[self.n - num])
                print("Move the %dth disks from %d to %d" % (num, start, end))
            elif end == 2:
                self.t2.push(self.disks[self.n - num])
                print("Move the %dth disks from %d to %d" % (num, start, end))
        #time.sleep(0.5)
        self.repaint()# 重画
        # self.update()


    #将n个盘子从start借助temp移动到end
    def moveTower(self, num, start, temp, end):
        if(num == 1):
            self.moveOneDisk(num, start, end)
        else:
            self.moveTower(num-1, start, end, temp) #将n-1个从start移动到temp
            self.moveOneDisk(num, start, end) #将第n个移动到end
            self.moveTower(num-1, temp, start, end) #将n-1个从temp移动到end

    def keyPressEvent(self, e):
        print(e.key)
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            # Enter为小键盘回车 Return为大键盘的回车
            self.moveTower(self.n, 1, 2, 3)
        if e.key() == Qt.Key_F1:
            self.showDialog()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, "Input Dialog", "Enter hanoi number:")
        if ok:
            if re.search("\\d+", text)==None:
                #正则表达式判断输入是否合法
                reply = QMessageBox.question(self, "Error!!", "Please ensure your input is a number", QMessageBox.Ok)
                if reply == QMessageBox.Ok:
                    self.showDialog()
            elif (int(text) > 64) or (int(text) < 1):
                reply = QMessageBox.question(self, "Warning!", "Please enter a number from 1 to 64", QMessageBox.Ok)
                if reply == QMessageBox.Ok:
                    self.showDialog()
            else:
                self.n = int(text)
                self.initTower()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main(64)
    sys.exit(app.exec_())
