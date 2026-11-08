from PyQt6 import QtCore, QtWidgets

class Label(QtWidgets.QLabel):

    canEdit = False
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
        selectable=False,
        **kwargs,
    ):
        self.m_data = data
        self.m_index = index
        self.m_element = element
        self.m_position = position
        self.m_selectable = selectable
        super().__init__(*args, **kwargs)
        self.setText(text)
        self.setData(data)
        self.adjustSize()

    def position(self):
        return self.m_position

    def isSelectable(self):
        return self.m_selectable

    def setData(self, data):
        if data:
            text = self.text()
            title = data.get("title", False)
            if title:
                text = text.title()
                self.setText(text)
            align = data.get("a")
            if align == "c":
                align = QtCore.Qt.AlignmentFlag.AlignCenter
            elif align == "l":
                align = QtCore.Qt.AlignmentFlag.AlignLeft
            elif align == "r":
                align = QtCore.Qt.AlignmentFlag.AlignRight
            if align:
                self.setAlignment(align)
