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

try:
    from ftrack_api import Session
except ImportError:
    print("Foi detectado que a API do ftrack não está instalada em seu sistema. Tentando instalar:")
    os.system("pip install ftrack-python-api")
    from ftrack_api import Session


# Lê a chave de API que está na pasta de TD
keyFile = 'admin' # passe pra cá o caminho do arquivo JSON escolhido
APIUser = '' # passe pra cá o nome do usuário, pego de dentro do arquivo JSON selecionado
APIKey = '' # passe pra cá a chave de API do usuário, pego de dentro do arquivo JSON selecionado


# Passa as informações necessárias de login para o ftrack
session = Session(
    server_url="https://hype.ftrackapp.com",
    api_key=APIKey,
    api_user=APIUser
)

projectQuery = session.query(
    'Project where status is "Active"'
).all()

for result in projectQuery:
    project = {
        'name': result['full_name'],
        'code': result['name'],
        'initials': result['custom_attributes']['initials']
    }
    print(project)


class Widget: 
    def __init__(self, *args):
        self.window = QWidget.QWidget()
        self.window.resize(600, 300)
        self.window.setWindowTitle("User Key Ftrack")
        vLayout = QWidget.QVBoxLayout()
        hLayout = QWidget.QHBoxLayout()
        self.keyList= QWidget.QlistWidget()
        self.userList=QWidget.QlistWidget()
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

    def show(self):
        self.window.show()


app = QWidget.QApplication(sys.argv)
    
ex = Widget()
ex.show()
sys.exit(app.exec_())



