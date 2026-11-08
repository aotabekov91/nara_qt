from PyQt6 import QtCore

import nara

class Model(nara.Model):

    loaded = QtCore.pyqtSignal(object)
    idChanged = QtCore.pyqtSignal(object)
    elementAdded = QtCore.pyqtSignal(object)
    elementWanted = QtCore.pyqtSignal(object)
    elementRemoved = QtCore.pyqtSignal(object)
    elementUpdated = QtCore.pyqtSignal(object)
    elementCreated = QtCore.pyqtSignal(object)

    def setId(self, idx):
        super().setId(idx)
        self.idChanged.emit(idx)

    def load(self):
        super().load()
        self.loaded.emit(self)

    def createElement(self, data={}, idx=None):
        element=super().createElement(data, idx)
        self.elementCreated.emit(element)
        return element

    def addElement(self, element):
        element=super().addElement(element)
        self.elementAdded.emit(element)
        return element

    def delElement(self, element):
        element=super().delElement(element)
        self.elementRemoved.emit(element)
        return element

    def updateElement(self, element, data):
        element=super().updateElement(element, data)
        self.elementUpdated.emit(element)
        return element
