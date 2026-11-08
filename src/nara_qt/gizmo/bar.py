from PyQt6 import QtCore, QtWidgets

from nara_qt import vimo

class StatusBarView(vimo.View, QtWidgets.QStatusBar):

    def setup(self):
        super().setup()
        self.setupProperties()
        self.setupContainer()
        self.show()

    def setupProperties(self):
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

    def setupContainer(self):
        self.container = QtWidgets.QWidget(
            objectName="Container")
        self.container.setContentsMargins(0, 0, 0, 0)
        self.addPermanentWidget(self.container, 10)
        self.m_layout = QtWidgets.QVBoxLayout(
            self.container)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        self.container.setLayout(self.m_layout)
        self.stack = QtWidgets.QStackedWidget(
            objectName="Stack")
        self.m_layout.addWidget(self.stack)
        self.setContentsMargins(0, 0, 3, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setSizeGripEnabled(False)
        self.layout().setSpacing(0)
        self.stack.hide()
        self.hide()

    def activate(self):
        self.show()

    def octivate(self):
        self.hide()

    def toggle(self):
        if self.isVisible():
            self.octivate()
        else:
            self.activate()
