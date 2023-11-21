# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets
from view import View
from Utils.tools import Tool


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,view=None,position=(0,0),dimension=(500,300)):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("CAI  2324A P2 : MainWindow (View) ")
        if view == None:
            print("MainWindow.__init__() :  need a view !")
            exit(0)
        self.view : View =view        
        scene=QtWidgets.QGraphicsScene() 
        self.view.setScene(scene)
        self.setCentralWidget(self.view)
        x,y=position
        w,h=dimension
        self.view.setGeometry(x,y,w,h)
        scene.setSceneRect(x,y,w,h) 
        # self.setGeometry(x,y,w,h)
        # self.view.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)

        self.create_actions()
        self.connect_actions()
        self.create_menus()
         
        # self.dock=QtWidgets.QDockWidget("Left Right Dock",self)
        # self.dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,self.dock)

    def get_view(self) :
        return self.view
    def set_view(self,view) :
        self.view=view
    def get_scene(self) :
        return self.view.scene()
 
    def create_actions(self) :
        # File actions
        # Action Open 
        self.action_file_open=QtWidgets.QAction(QtGui.QIcon('Icons/open.png'),"Open",self)
        self.action_file_open.setShortcut("Ctrl+O")
        self.action_file_open.setStatusTip("Open file")
        # Action Exit
        self.action_exit=QtWidgets.QAction(QtGui.QIcon('Icons/exit.png'),"Exit",self)
        self.action_exit.setShortcut("Ctrl+Q")
        self.action_exit.setStatusTip("Exit")
        
        # Tools actions
        self.action_tools=QtWidgets.QActionGroup(self)
        # Line tool
        self.action_tools_line=QtWidgets.QAction(self.tr("&Line"),self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)
        # Rectangle tool
        self.action_tools_rect=QtWidgets.QAction(self.tr("&Rect"),self)
        self.action_tools_rect.setCheckable(True)
        self.action_tools.addAction(self.action_tools_rect)
        # Ellipse tool
        self.action_tools_ellip=QtWidgets.QAction(self.tr("&Ellipse"),self)
        self.action_tools_ellip.setCheckable(True)
        self.action_tools.addAction(self.action_tools_ellip)
        # Poly tool
        self.action_tools_poly=QtWidgets.QAction(self.tr("&Polygon"),self)
        self.action_tools_poly.setCheckable(True)
        self.action_tools.addAction(self.action_tools_poly)
        # Text tool
        self.action_tools_text=QtWidgets.QAction(self.tr("&Text"),self)
        self.action_tools_text.setCheckable(True)
        self.action_tools.addAction(self.action_tools_text)


        # Style actions    
        # self.action_style=QtWidgets.QActionGroup(self)
        self.action_pen_color_style=QtWidgets.QAction(self.tr("&Color"),self)
        self.action_brush_color_style=QtWidgets.QAction(self.tr("&Color"),self)


        # Help actions    
    def connect_actions(self) :
        # File menu
        self.action_file_open.triggered.connect(self.file_open)
        self.action_exit.triggered.connect(exit)
        
        # Tools menu
        self.action_tools_line.triggered.connect(
            lambda checked,tool=Tool.LINE: self.tools_selection(checked,tool)
        )
        self.action_tools_rect.triggered.connect(
            lambda checked,tool=Tool.RECTANGLE: self.tools_selection(checked,tool)
        )
        self.action_tools_ellip.triggered.connect(
            lambda checked,tool=Tool.ELLIPSE: self.tools_selection(checked,tool)
        )
        self.action_tools_poly.triggered.connect(
            lambda checked,tool=Tool.POLYGON: self.tools_selection(checked,tool)
        )
        self.action_tools_text.triggered.connect(
            lambda checked,tool=Tool.TEXT: self.tools_selection(checked,tool)
        )
        # Style
        self.action_pen_color_style.triggered.connect(self.style_pen_color_selection)
        self.action_brush_color_style.triggered.connect(self.style_brush_color_selection)
        

    # Actions 
    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", os.getcwd())
        fileopen=QtCore.QFile(filename[0])
        print("open",fileopen)

    def tools_selection(self,checked,tool) :
        print("MainWindow.action_set_tools()")
        print("checked : ",checked)
        print("tool : ",tool)
        self.view.select_tool(tool)

    def style_pen_color_selection(self):
        color  = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self)
        if color.isValid():
            self.view.select_pen_color(color=color.name())
    def style_brush_color_selection(self):
        color  = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self)
        if color.isValid():
            self.view.select_brush_color(color=color.name())

    def create_menus(self) :
        # Menubar actions
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(self.action_file_open)
        menu_file.addAction(self.action_exit)

        menu_tools = menubar.addMenu('&Tools')
        menu_tools.addAction(self.action_tools_line)
        menu_tools.addAction(self.action_tools_rect)
        menu_tools.addAction(self.action_tools_ellip)
        menu_tools.addAction(self.action_tools_poly)
        menu_tools.addAction(self.action_tools_text)
        
        menu_style = menubar.addMenu('&Style')
        menu_style_pen = menu_style.addMenu('&Pen')
        menu_style_pen.addAction(self.action_pen_color_style)
        menu_style_brush = menu_style.addMenu('&Brush')
        menu_style_brush.addAction(self.action_brush_color_style)
        
        
        # Toolbar actions
        toolbar=self.addToolBar("File")
        toolbar.addAction(self.action_file_open)
        toolbar=self.addToolBar("Tools")
        toolbar.addAction(self.action_tools_line)
        toolbar.addAction(self.action_tools_rect)
        toolbar.addAction(self.action_tools_ellip)
        toolbar.addAction(self.action_tools_poly)
        toolbar.addAction(self.action_tools_text)
        # Style



        
    def resizeEvent(self, event):
        print("MainWindow.resizeEvent() : View")
        if self.view :
            print("dx : ",self.size().width()-self.view.size().width())
            print("dy : ",self.size().height()-self.view.size().height())
        else :
            print("MainWindow need  a scene !!!!! ")
        print("menubar size : ", self.menuBar().size())

if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)

    view=View()
    position=0,0
    dimension=600,400
    main=MainWindow(view,position,dimension)

    xd,yd=0,0
    xf,yf=200,100
    line=QtWidgets.QGraphicsLineItem(xd,yd,xf,yf)
    line.setPen(view.get_pen())
    view.scene().addItem(line)

    main.show()

    sys.exit(app.exec_())
