#!/usr/bin/python
import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from Utils.tools import Tool
from PyQt5.QtGui import QPolygonF

class EditableTextItem(QtWidgets.QGraphicsTextItem):
    def __init__(self, text="Double-click to edit text"):
        super().__init__(text)
        self.setFlag(QtWidgets.QGraphicsTextItem.ItemIsSelectable)
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        super().focusOutEvent(event)



class View (QtWidgets.QGraphicsView) :
    def __init__(self,position=(0,0),dimension=(600,400)):
        QtWidgets.QGraphicsView.__init__(self)
        x,y=position
        w,h=dimension
        self.setGeometry(x,y,w,h)

        self.begin,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.offset=QtCore.QPoint(0,0)
        self.tool=Tool.LINE
        self.item=None
        self.polygonPointsSets = []  # Initialize an empty list for sets of polygon points
        self.currentPolygonPoints = []  # Current working polygon points
        self.pen,self.brush=None,None
        self.pen_thickness = 1
        self.create_style()

    def __repr__(self):
        return "<View({},{},{})>".format(self.pen,self.brush,self.tool)
    
    def get_pen(self) :
        return self.pen
    def set_pen(self,pen) :
        self.pen=pen
    def get_brush(self) :
        return self.brush
    def set_brush(self,brush) :
        self.brush=brush

    def create_style(self) :
        self.create_pen()
        self.create_brush()
     
    def create_pen(self) :
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
    def create_brush(self) :
        self.brush=QtGui.QBrush()
        self.brush.setColor(QtCore.Qt.blue)
        self.brush.setStyle(QtCore.Qt.CrossPattern)
    
    def select_tool(self,tool) :
        print("View.set_tool(self,tool)",tool)
        self.tool=tool
    def select_pen_color(self,color) :
        print("View.set_pen_color(self,color)",color)
        self.pen.setColor(QtGui.QColor(color))
    def select_brush_color(self,color) :
        print("View.set_brush_color(self,color)",color)
        self.brush.setColor(QtGui.QColor(color))
    def set_pen_thickness(self, thickness):
        self.pen_thickness = thickness
        if self.pen:
            self.pen.setWidth(self.pen_thickness)
            self.update()

    # events
    def mousePressEvent(self, event):
        print("View.mousePressEvent()")
        print("event.pos() : ",event.pos())
        print("event.screenPos() : ",event.screenPos())
        self.begin=self.end=event.pos()
        if self.scene() :
            self.item=self.scene().itemAt(self.begin,QtGui.QTransform())
            if self.item :
                self.offset =self.begin-self.item.pos()
            if self.tool == Tool.POLYGON and self.scene():
                self.currentPolygonPoints.append(event.pos())

    def mouseMoveEvent(self, event):
        self.end=event.pos()
        if self.scene() :
            if self.item :
                self.item.setPos(event.pos() - self.offset)
            else :
                print("draw bounding box !")
        else :
            print("no scene associated !")
    def mouseReleaseEvent(self, event):
        print("View.mouseReleaseEvent()")
        print("nb items : ",len(self.items()))
        self.end=event.pos()        
        if self.scene() :
            if self.item :
                self.item.setPos(event.pos() - self.offset)
                self.item=None
            elif self.tool==Tool.LINE :
                line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
                line.setPen(self.pen)
                self.scene().addItem(line)
            elif self.tool==Tool.RECTANGLE :
                rect=QtWidgets.QGraphicsRectItem(
                                    self.begin.x(),self.begin.y(),
                                    abs(self.end.x()-self.begin.x()),
                                    abs(self.end.y()-self.begin.y())
                            )
                rect.setPen(self.pen)
                rect.setBrush(self.brush)
                self.scene().addItem(rect)
            
            elif self.tool == Tool.ELLIPSE:
                ellipse = QtWidgets.QGraphicsEllipseItem(
                    self.begin.x(), self.begin.y(),
                    abs(self.end.x() - self.begin.x()),
                    abs(self.end.y() - self.begin.y())
                )
                ellipse.setPen(self.pen)
                ellipse.setBrush(self.brush)
                self.scene().addItem(ellipse)

            
            elif self.tool == Tool.TEXT:
                # Create an EditableTextItem instead of a regular QGraphicsTextItem
                textItem = EditableTextItem("Double-click to edit text")
                textItem.setPos(self.begin)
                self.scene().addItem(textItem)


            elif self.tool == Tool.POLYGON and self.scene():
                if len(self.currentPolygonPoints) > 1:
                    # Draw temporary lines between current polygon points
                    temp_line = QtWidgets.QGraphicsLineItem(
                        QtCore.QLineF(self.currentPolygonPoints[-2], self.currentPolygonPoints[-1]))
                    temp_line.setPen(self.pen)
                    self.scene().addItem(temp_line)

            else :
                print("nothing to draw !")

    def mouseDoubleClickEvent(self, event):
        if self.tool == Tool.POLYGON:
            self.finalizeCurrentPolygon()
        
        if self.tool == Tool.TEXT:
            # Find the text item under the mouse cursor
            text_item = self.scene().itemAt(event.pos(), QtGui.QTransform())
            if isinstance(text_item, EditableTextItem):
                # Set the focus to the text item
                text_item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
                text_item.setFocus(QtCore.Qt.MouseFocusReason)

    def finalizeCurrentPolygon(self):
        # Finalize the current polygon
        if self.tool == Tool.POLYGON and self.scene() and self.currentPolygonPoints:
            polygon = QPolygonF(self.currentPolygonPoints)
            polygonItem = QtWidgets.QGraphicsPolygonItem(polygon)
            polygonItem.setPen(self.pen)
            self.scene().addItem(polygonItem)
            self.polygonPointsSets.append(self.currentPolygonPoints)
            self.currentPolygonPoints = []  # Clear the current points list for a new polygon

    def resizeEvent(self,event):
        print("View.resizeEvent()")
        print("width : {}, height : {}".format(self.size().width(),self.size().height()))
   
if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)

    # View
    x,y=0,0
    w,h=600,400
    view=View(position=(x,y),dimension=(w,h))
    view.setWindowTitle("CAI : View v1.0")

    # Scene
    model=QtWidgets.QGraphicsScene()
    model.setSceneRect(x,y,w,h)
    view.setScene(model)
    # view.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)

    # Items
    xd,yd=0,0
    xf,yf=200,300
    line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
    line.setPen(view.get_pen())
    model.addItem(line)

    view.show()
    sys.exit(app.exec_())

