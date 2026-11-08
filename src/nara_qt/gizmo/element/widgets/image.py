import os

from PyQt6 import QtCore, QtGui

from .label import Label

class Image(Label):

    def setData(self, data):
        if not data:
            return
        if not self.m_element:
            return
        align = data.get("a", "c")
        edata = self.m_element.data()
        self.m_path = edata.get("image", None)
        if not self.m_path:
            return
        if not os.path.exists(self.m_path):
            return
        if align == "c":
            align = QtCore.Qt.AlignmentFlag.AlignCenter
        elif align == "l":
            align = QtCore.Qt.AlignmentFlag.AlignLeft
        elif align == "r":
            align = QtCore.Qt.AlignmentFlag.AlignRight
        self.setAlignment(align)
        pxm = QtGui.QPixmap(self.m_path)
        self.setPixmap(pxm)
