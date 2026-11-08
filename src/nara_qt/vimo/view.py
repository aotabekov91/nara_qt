from PyQt6 import QtCore

import nara

class View(nara.View):

    cleanUpWanted = QtCore.pyqtSignal()
    viewIsRedrawn = QtCore.pyqtSignal()
    resized = QtCore.pyqtSignal(object)
    painted = QtCore.pyqtSignal(object, object)
    focusLost = QtCore.pyqtSignal(object)
    focusGained = QtCore.pyqtSignal(object)
    closeWanted = QtCore.pyqtSignal(object)
    modelLoaded = QtCore.pyqtSignal(object, object)
    modelChanged = QtCore.pyqtSignal(object)
    indexChanged = QtCore.pyqtSignal(object)
    posIndexChanged = QtCore.pyqtSignal(
        object, object, object)
    identifierChanged = QtCore.pyqtSignal(
        object, object, object)
    geometryChanged = QtCore.pyqtSignal()
    modelIsToBeChanged = QtCore.pyqtSignal(object, object)
    viewIsToBeRedrawn = QtCore.pyqtSignal()

    def setup(self):
        super().setup()
        self.setBars()
        if hasattr(self, "setParent"):
            self.setParent(self.m_parent)
        if hasattr(self, "setObjectName"):
            oname = self.m_objectName or self.name
            self.setObjectName(oname)

    def setIdentifier(self, idx):
        o = self.m_vid
        self.m_vid = idx
        self.identifierChanged.emit(idx, o, self)

    def setBars(self):
        func = "horizontalScrollBarPolicy"
        if not hasattr(self, func):
            return
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def setChild(self, obj):
        super().setChild(obj)
        obj.identifierChanged.connect(self.updateChildIndex)
        obj.posIndexChanged.connect(self.updateChildIndex)

    def betChild(self, obj):
        c = super().betChild(obj)
        if not c:
            return
        c.posIndexChanged.disconnect()
        c.identifierChanged.disconnect()
        return c

    def setIndex(self, index=None):
        self.m_id = index
        self.indexChanged.emit(index)

    def setPosIndex(self, idx=None):
        old = self.m_pid
        self.m_pid = idx
        self.posIndexChanged.emit(idx, old, self)

    def setModel(self, model):
        if id(self.m_model) != id(model):
            self.modelIsToBeChanged.emit(self, self.m_model)
            self.m_model = model
            self.kind = model.kind
            self.modelChanged.emit(model)

    def cleanUp(self):
        self.cleanUpWanted.emit()

    def redraw(self):
        self.viewIsRedrawn.emit()

    def resetConfigure(self, **kwargs):
        pass

    def event(self, event):
        if hasattr(super(), 'event'):
            result = super().event(event)
            if event.type() == QtCore.QEvent.Type.Resize:
                self.resized.emit(self)
            if event.type() == QtCore.QEvent.Type.Paint:
                self.painted.emit(self, event)
            return result
        return False

    def show(self, *args, **kwargs):
        super().show()
