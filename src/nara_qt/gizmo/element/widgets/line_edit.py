from PyQt6 import QtCore, QtGui, QtWidgets

class LineEdit(QtWidgets.QLineEdit):

    canEdit = True
    focusGained = QtCore.pyqtSignal()
    geometryChanged = QtCore.pyqtSignal()

    def __init__(
        self,
        *args,
        data=None,
        text=None,
        index=None,
        title=False,
        element=None,
        position=None,
        wait_time=1000,
        selectable=True,
        **kwargs,
    ):
        self.m_data = data
        self.m_index = index
        self.m_wait = wait_time
        self.m_element = element
        self.m_reporting = False
        self.m_position = position
        self.m_selectable = selectable
        super().__init__(*args, **kwargs)
        if text:
            self.setText(text)
        self.textChanged.connect(self.on_textChanged)
        self.setInputMode()
        self.adjustSize()
        self.setTimer()

    def on_textChanged(self):
        self.timer.stop()
        self.geometryChanged.emit()
        if self.m_reporting:
            self.timer.start(self.m_wait)

    def setTimer(self):
        self.m_reporting = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateElementData)

    def updateElementData(self):
        t = self.text()
        self.timer.stop()
        d = self.m_element.data()
        d.update({self.m_index: t})
        model = self.m_element.model()
        if model:
            model.elementUpdated.emit(self.m_element)

    def position(self):
        return self.m_position

    def isSelectable(self):
        return self.m_selectable

    def setInputMode(
        self,
        cond=False,
        mode=None,
    ):
        self.setReadOnly(not cond)
        if cond:
            self.setFocus()
            if mode == "append":
                pos = Qt.CursorShape.ui.QTextCursor.End
                c = self.textCursor()
                c.movePosition(pos)
                self.setTextCursor(c)

    def setFocus(self):
        super().setFocus()
        self.focusGained.emit()
