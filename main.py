# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtGui,QtWidgets

from view import View
from main_window import MainWindow

print(QtCore.QT_VERSION_STR)

app=QtWidgets.QApplication(sys.argv)
view=View()
position=0,0
dimension=600,400
main=MainWindow(view,position,dimension)

xd,yd=0,0
xf,yf=200,100
line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
pen=QtGui.QPen()
pen.setColor(QtCore.Qt.red)
line.setPen(pen)
view.scene().addItem(line)

main.show()

sys.exit(app.exec_())
