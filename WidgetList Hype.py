import os
import sys

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
)
except ImportError:
    os.system("pip install -U PySide2")
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
)

class Widget: 
    def __init__(self, *args):
        self.window = QtGui.QWidget()
        self.window.resize(600, 300)
        self.window.setWindowTitle("User Key Ftrack")
        vLayout = QtGui.QVBoxLayout()
        hLayout = QtGui.QHBoxLayout()
        self.keyList= QtGui.QlistWidget()
        self.userList=QtGui.QlistWidget()
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)


        for n, tabName in enumerate(["Users", "Keys"]):
            tabs.addTab(tabName)

        self.setCentralWidget(tabs)

        

        for data["api_key"] in data:
            keyList.addItem(data["api_key"])

        for data["api_user"] in data:
            userList.AddItem(data["api_user"])    


        hLayout.addWidget(keyList, Color('red'))
        hLayout.addWidget(userList, Color ('green'))

        
        
    def getKey(self, *args):
       api_key= self.keyList.itemPressed()
       api_user= self.userList.ItemPressed()
       print (api_user)
       print (api_key)
       print("change Key and User")

       if api_key== '':
            api_key=data["api_key"]
            print ("api key deafault")
            print= data["api_key"]

       if api_user=='':
            api_user= data["api_user"]
            print ("api user deafault")
            print= data["api_user"]

    def show(self):
        self.window.show()

app = QtGui.QApplication(sys.argv)
    
ex = Widget()
ex.getKey()
ex.show()
sys.exit(app.exec_())



