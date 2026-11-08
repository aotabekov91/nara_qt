from PyQt6 import QtCore, QtWidgets

from .utils import setEditorTabSize

class TextEdit(QtWidgets.QTextEdit):

    canEdit = True
    focusGained = QtCore.pyqtSignal()
    geometryChanged = QtCore.pyqtSignal()

    def __init__(
        self,
        *args,
        data=None,
        text=None,
        index=None,
        parent=None,
        element=None,
        position=None,
        wait_time=1000,
        selectable=True,
        **kwargs,
    ):
        self.m_data = data
        self.m_index = index
        self.m_parent = parent
        self.m_wait = wait_time
        self.m_reporting = False
        self.m_element = element
        self.m_position = position
        self.m_selectable = selectable
        super().__init__(*args, **kwargs)
        if text:
            self.setText(text)
        self.textChanged.connect(self.on_textChanged)
        setEditorTabSize(self, 4)
        self.setReadOnly(True)
        self.adjustSize()
        self.setTimer()
        self.setBars()

    def position(self):
        return self.m_position

    def isSelectable(self):
        return self.m_selectable

    def setTimer(self):
        self.m_reporting = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateElementData)

    def on_textChanged(self):
        self.timer.stop()
        self.geometryChanged.emit()
        if self.m_reporting:
            self.timer.start(self.m_wait)

    def updateElementData(self):
        self.timer.stop()
        t = self.toPlainText()
        d = self.m_element.data()
        d.update({self.m_index: t})
        model = self.m_element.model()
        if model:
            model.elementUpdated.emit(self.m_element)

    def sizeHint(self):
        h = super().sizeHint()
        doc = self.document()
        size = doc.size().toSize()
        height = max(5, size.height())
        # h.setHeight(height+15)
        h.setHeight(height)
        return h

    def setBars(self):
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def setFocus(self):
        super().setFocus()
        self.focusGained.emit()
