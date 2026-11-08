from PyQt6 import QtCore, QtWidgets

from nara_qt import vimo

class WindowView(vimo.View, QtWidgets.QMainWindow):

    def setup(self):
        super().setup()
        self.setProperties()
        self.container = QtWidgets.QWidget(
            objectName="MainWindowContainer")
        self.m_layout = QtWidgets.QVBoxLayout()
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        self.container.setLayout(self.m_layout)
        self.setCentralWidget(self.container)
        self.setContentsMargins(0, 0, 0, 0)

    def setProperties(self):
        self.setAcceptDrops(True)
        self.setMinimumSize(800, 600)
        #self.setWindowFlags(
        #    QtCore.Qt.WindowType.FramelessWindowHint)
        #self.setAttribute(
        #    QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
