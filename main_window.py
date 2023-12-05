# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets
from view import View
from Utils.tools import Tool
import json

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
        # Action Save 
        self.action_save = QtWidgets.QAction(QtGui.QIcon('Icons/save.png'), "Save", self)
        self.action_save.setShortcut("Ctrl+S")
        self.action_save.setStatusTip("Save the scene")
        # Action Load
        self.action_load = QtWidgets.QAction(QtGui.QIcon('Icons/load.png'), "Load", self)
        self.action_load.setShortcut("Ctrl+L")
        self.action_load.setStatusTip("Load a scene")
        # Action Clear
        self.action_clear=QtWidgets.QAction(QtGui.QIcon('Icons/clear.png'),"Clear",self)
        self.action_clear.setShortcut("Ctrl+Shift+C")
        self.action_clear.setStatusTip("Clear")


        # Tools actions
        self.action_tools=QtWidgets.QActionGroup(self)
        # Line tool
        self.action_tools_line=QtWidgets.QAction(QtGui.QIcon('Icons/tool_line.png'),self.tr("&Line"),self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)
        # Rectangle tool
        self.action_tools_rect=QtWidgets.QAction(QtGui.QIcon('Icons/tool_rectangle.png'),self.tr("&Rect"),self)
        self.action_tools_rect.setCheckable(True)
        self.action_tools.addAction(self.action_tools_rect)
        # Ellipse tool
        self.action_tools_ellip=QtWidgets.QAction(QtGui.QIcon('Icons/tool_ellipse.png'),self.tr("&Ellipse"),self)
        self.action_tools_ellip.setCheckable(True)
        self.action_tools.addAction(self.action_tools_ellip)
        # Poly tool
        self.action_tools_poly=QtWidgets.QAction(QtGui.QIcon('Icons/tool_polygon.png'),self.tr("&Polygon"),self)
        self.action_tools_poly.setCheckable(True)
        self.action_tools.addAction(self.action_tools_poly)
        # Text tool
        self.action_tools_text=QtWidgets.QAction(QtGui.QIcon('Icons/tool_text.png'),self.tr("&Text"),self)
        self.action_tools_text.setCheckable(True)
        self.action_tools.addAction(self.action_tools_text)

        # Style actions    
        # Pen Style    
        self.action_pen_color_style=QtWidgets.QAction(QtGui.QIcon('Icons/colorize.png'),self.tr("&Color"),self)
        self.action_pen_thickness = QtWidgets.QAction(self.tr("&Thickness"), self)
        self.action_pen_solid = QtWidgets.QAction("Solid Line", self)
        self.action_pen_dash = QtWidgets.QAction("Dash Line", self)
        self.action_pen_dot = QtWidgets.QAction("Dot Line", self)
        # Brush Styles
        self.action_brush_color_style=QtWidgets.QAction(QtGui.QIcon('Icons/colorize.png'),self.tr("&Color"),self)
        self.action_brush_solid = QtWidgets.QAction("Solid Brush", self)
        self.action_brush_dense = QtWidgets.QAction("Dense Brush", self)
        self.action_brush_diag = QtWidgets.QAction("Diagonal Brush", self)
        

        # Help 
        self.action_help=QtWidgets.QActionGroup(self)
        self.action_help_aboutus=QtWidgets.QAction(self.tr("&About Us"),self)



        # Help actions    
    def connect_actions(self) :
        # File menu
        self.action_file_open.triggered.connect(self.file_open)
        self.action_exit.triggered.connect(self.quit_app)
        self.action_file_open.triggered.connect(self.file_load)
        self.action_save.triggered.connect(self.file_save)
        self.action_load.triggered.connect(self.file_load)
        self.action_clear.triggered.connect(self.clear_scene)

        
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
        self.action_pen_thickness.triggered.connect(self.style_pen_thickness_selection)
        self.action_pen_solid.triggered.connect(lambda: self.change_pen_style(QtCore.Qt.SolidLine))
        self.action_pen_dash.triggered.connect(lambda: self.change_pen_style(QtCore.Qt.DashLine))
        self.action_pen_dot.triggered.connect(lambda: self.change_pen_style(QtCore.Qt.DotLine))

        self.action_brush_solid.triggered.connect(lambda: self.change_brush_style(QtCore.Qt.SolidPattern))
        self.action_brush_dense.triggered.connect(lambda: self.change_brush_style(QtCore.Qt.Dense1Pattern))
        self.action_brush_diag.triggered.connect(lambda: self.change_brush_style(QtCore.Qt.DiagCrossPattern))
        # Help
        self.action_help_aboutus.triggered.connect(self.about_us)

    # Actions 

    def style_pen_thickness_selection(self):
        # Create a dialog to set the pen thickness
        dialog = QtWidgets.QInputDialog(self)
        dialog.setInputMode(QtWidgets.QInputDialog.IntInput)
        dialog.setIntRange(1, 10)  # Set the allowed range for pen thickness
        dialog.setIntValue(1)  # Set the default value
        dialog.setWindowTitle("Pen Thickness")
        dialog.setLabelText("Select Pen Thickness:")
        if dialog.exec_():
            # Get the selected pen thickness
            pen_thickness = dialog.intValue()
            self.view.set_pen_thickness(pen_thickness)


    def quit_app(self):
        reply = QtWidgets.QMessageBox.question(self, 'Quit', 
                                            "Are you sure you want to quit the scene?",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                                            QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.destroy()
            exit()
        

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
            self.view.set_pen_thickness(self.view.pen_thickness)  # Set the pen thickness

    def style_brush_color_selection(self):
        color  = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self)
        if color.isValid():
            self.view.select_brush_color(color=color.name())
    
    def about_us(self):
        # Create a dialog
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("About Us")
        layout = QtWidgets.QVBoxLayout(dialog)
        about_text = QtWidgets.QLabel("Realise par :\n\n "
                                    "- Bahlak Mohamed Zahed\n"
                                    "- Achak Ayoub\n")
        about_text.setWordWrap(True)
        layout.addWidget(about_text)
        close_button = QtWidgets.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def file_save(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "JSON Files (*.json)")
        if not filename:
            return  # User cancelled the save

        items_data = []
        for item in self.view.scene().items():
            item_data = {
                'type': 'unknown',
            }

            if isinstance(item, QtWidgets.QGraphicsLineItem) or \
            isinstance(item, QtWidgets.QGraphicsRectItem) or \
            isinstance(item, QtWidgets.QGraphicsEllipseItem) or \
            isinstance(item, QtWidgets.QGraphicsPolygonItem):
                item_data['pen'] = {
                    'color': item.pen().color().name(),
                    'width': item.pen().width(),
                    'style': item.pen().style()
                }

            if isinstance(item, QtWidgets.QGraphicsLineItem):
                item_data.update({
                    'type': 'line',
                    'start': {'x': item.line().x1(), 'y': item.line().y1()},
                    'end': {'x': item.line().x2(), 'y': item.line().y2()}
                })
            elif isinstance(item, QtWidgets.QGraphicsRectItem):
                item_data.update({
                    'type': 'rectangle',
                    'topLeft': {'x': item.rect().topLeft().x(), 'y': item.rect().topLeft().y()},
                    'bottomRight': {'x': item.rect().bottomRight().x(), 'y': item.rect().bottomRight().y()},
                    'brush': {
                        'color': item.brush().color().name(),
                        'style': item.brush().style()
                    }
                })
            elif isinstance(item, QtWidgets.QGraphicsEllipseItem):
                item_data.update({
                    'type': 'ellipse',
                    'center': {'x': item.rect().center().x(), 'y': item.rect().center().y()},
                    'radiusH': item.rect().width() / 2,
                    'radiusV': item.rect().height() / 2,
                    'brush': {
                        'color': item.brush().color().name(),
                        'style': item.brush().style()
                    }
                })
            elif isinstance(item, QtWidgets.QGraphicsPolygonItem):
                points = [{'x': p.x(), 'y': p.y()} for p in item.polygon()]
                item_data.update({
                    'type': 'polygon',
                    'points': points
                })
            elif isinstance(item, QtWidgets.QGraphicsTextItem):
                item_data.update({
                    'type': 'text',
                    'text': item.toPlainText(),
                    'position': {'x': item.pos().x(), 'y': item.pos().y()},
                    'color': item.defaultTextColor().name()
                })

            items_data.append(item_data)

        with open(filename, 'w') as file:
            json.dump(items_data, file, indent=4)



    def file_load(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "JSON Files (*.json)")
        if not filename:
            return  # User cancelled the load

        with open(filename, 'r') as file:
            items_data = json.load(file)

        scene = self.view.scene()
        scene.clear()  # Clear existing items before loading new ones

        for item_data in items_data:
            pen = QtGui.QPen(QtGui.QColor(item_data['pen']['color']), item_data['pen']['width'], item_data['pen']['style']) if 'pen' in item_data else None
            if item_data['type'] == 'line':
                line = QtCore.QLineF(item_data['start']['x'], item_data['start']['y'],
                                    item_data['end']['x'], item_data['end']['y'])
                line_item = QtWidgets.QGraphicsLineItem(line)
                pen and line_item.setPen(pen)
                scene.addItem(line_item)

            elif item_data['type'] == 'rectangle':
                rect = QtCore.QRectF(QtCore.QPointF(item_data['topLeft']['x'], item_data['topLeft']['y']),
                                    QtCore.QPointF(item_data['bottomRight']['x'], item_data['bottomRight']['y']))
                rect_item = QtWidgets.QGraphicsRectItem(rect)
                pen and rect_item.setPen(pen)
                ('brush' in item_data) and rect_item.setBrush(QtGui.QBrush(QtGui.QColor(item_data['brush']['color']),
                                                    item_data['brush']['style']))
                scene.addItem(rect_item)

            elif item_data['type'] == 'ellipse':
                center = QtCore.QPointF(item_data['center']['x'], item_data['center']['y'])
                ellipse = QtCore.QRectF(center.x() - item_data['radiusH'], center.y() - item_data['radiusV'],
                                        item_data['radiusH'] * 2, item_data['radiusV'] * 2)
                ellipse_item = QtWidgets.QGraphicsEllipseItem(ellipse)
                pen and ellipse_item.setPen(pen)
                ('brush' in item_data) and ellipse_item.setBrush(QtGui.QBrush(QtGui.QColor(item_data['brush']['color']),
                                                    item_data['brush']['style']))
                scene.addItem(ellipse_item)

            elif item_data['type'] == 'polygon':
                polygon = QtGui.QPolygonF([QtCore.QPointF(p['x'], p['y']) for p in item_data['points']])
                polygon_item = QtWidgets.QGraphicsPolygonItem(polygon)
                pen and polygon_item.setPen(pen)
                scene.addItem(polygon_item)

            elif item_data['type'] == 'text':
                text_item = QtWidgets.QGraphicsTextItem(item_data['text'])
                text_item.setPos(QtCore.QPointF(item_data['position']['x'], item_data['position']['y']))
                # Text color is handled differently
                text_color = QtGui.QColor(item_data['color']) if 'color' in item_data else QtGui.QColor('black')
                text_item.setDefaultTextColor(text_color)
                scene.addItem(text_item)


    def clear_scene(self):
        reply = QtWidgets.QMessageBox.question(self, 'Clear Scene', 
                                            "Are you sure you want to clear the scene?",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                                            QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            scene = self.view.scene()
            scene.clear()
        else:
            print("Scene clear cancelled.")
    
    def change_pen_style(self, style):
        if self.view and self.view.get_pen():
            pen = self.view.get_pen()
            pen.setStyle(style)
            self.view.set_pen(pen)

    def change_brush_style(self, style):
        if self.view and self.view.get_brush():
            brush = self.view.get_brush()
            brush.setStyle(style)
            self.view.set_brush(brush)


    def create_menus(self) :
        # Menubar actions
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(self.action_file_open)
        menu_file.addAction(self.action_save)
        menu_file.addAction(self.action_load)
        menu_file.addAction(self.action_clear)
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
        menu_style_pen.addAction(self.action_pen_thickness)
        menu_style_pen.addAction(self.action_pen_solid)
        menu_style_pen.addAction(self.action_pen_dash)
        menu_style_pen.addAction(self.action_pen_dot)

        menu_style_brush = menu_style.addMenu('&Brush')
        menu_style_brush.addAction(self.action_brush_color_style)
        menu_style_brush.addAction(self.action_brush_solid)
        menu_style_brush.addAction(self.action_brush_dense)
        menu_style_brush.addAction(self.action_brush_diag)
        
        menu_help = menubar.addMenu('&Help')
        menu_help.addAction(self.action_help_aboutus)
        
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
