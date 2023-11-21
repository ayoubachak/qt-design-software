#!/usr/bin/python
import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from Utils.tools import Tool


class Scene (QtWidgets.QGraphicsScene) :
    def __init__(self):
        QtWidgets.QGraphicsScene.__init__(self)
        self.begin,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.offset=QtCore.QPoint(0,0)
        self.tool=Tool.RECTANGLE
        self.item=None
        self.pen,self.brush=None,None
        self.create()

    def __repr__(self):
        return "<Scene({},{},{})>".format(self.pen,self.brush,self.tool)
    def create(self) :
        self.create_pen()
        self.create_brush()
     
    def create_pen(self) :
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
    def create_brush(self) :
        self.brush=QtGui.QBrush()
        self.brush.setColor(QtCore.Qt.blue)
        self.brush.setStyle(QtCore.Qt.CrossPattern)

    def create_line(self,start=(0,0),end=(100,100)) :
        x,y=start
        w,h=end
        line=QtWidgets.QGraphicsLineItem(x,y,w,h)
        line.setPen(self.pen)
        self.addItem(line)
    def create_rect(self,position=(0,0),dimension=(100,100)) :
        x,y=position
        w,h=dimension
        rect=QtWidgets.QGraphicsRectItem(x,y,w,h)
        rect.setPen(self.pen)
        rect.setBrush(self.brush)
        self.addItem(rect)
        # rect.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable|QtWidgets.QGraphicsItem.ItemIsSelectable )


    def set_tool(self,tool) :
        print("Scene.set_tool(self,tool)",tool)
        self.tool=tool

    def set_pen_color(self,color) :
        print("Scene.set_pen_color(self,color)",color)
        self.pen.setColor(color)
    def set_brush_color(self,color) :
        print("Scene.set_brush_color(self,color)",color)
        self.brush.setColor(color)
    # events
    def mousePressEvent(self, event):
        print("Scene.mousePressEvent()")
        print("event.scenePos() : ",event.scenePos())
        print("event.screenPos() : ",event.screenPos())
        self.begin=self.end=event.scenePos()
        self.item=self.itemAt(self.begin,QtGui.QTransform())
        if self.item :
            self.offset =self.begin-self.item.pos()                
    def mouseMoveEvent(self, event):
        print("items number : ",len(self.items()))
        print("pen : ",self.pen)
        self.end = event.scenePos()
        if self.item :
            self.item.setPos(event.scenePos() - self.offset)
        else :
            print("nothing to move !")
    def mouseReleaseEvent(self, event):
        print("items number : ",len(self.items()))
        print("pen : ",self.pen)
        self.end = event.scenePos()
        if self.item :
            self.item.setPos(event.scenePos() - self.offset)
            self.item=None
        elif self.tool==Tool.LINE :
            line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
            line.setPen(self.pen)
            self.addItem(line)
        elif self.tool==Tool.RECTANGLE :
            rect=QtWidgets.QGraphicsRectItem(
                                self.begin.x(),self.begin.y(),
                                self.end.x()-self.begin.x(),
                                self.end.y()-self.begin.y()
                        )
            rect.setPen(self.pen)
            rect.setBrush(self.brush)
            self.addItem(rect)
        else :
            print("nothing to draw !")

    def resizeEvent(self,event):
        print("Scene.resizeEvent()")
    
if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    model=Scene()
    x,y=0,0
    w,h=600,400
    model.create()
    view=QtWidgets.QGraphicsView()
    view.setGeometry(x,y,w,h)
    model.setSceneRect(x,y,w,h)
    view.setScene(model)
    # scene.setSceneRect(x-50,y-50,width,height)
    view.show()
    sys.exit(app.exec_())

