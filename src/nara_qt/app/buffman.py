import typing as tp
from PyQt6 import QtCore

import nara

class Buffman(nara.Buffman, QtCore.QObject):

    modelCreated: QtCore.pyqtSignal = QtCore.pyqtSignal(object)
    viewAdded = QtCore.pyqtSignal(object)
    viewClosed = QtCore.pyqtSignal(object)
    posIndexChanged = QtCore.pyqtSignal(object, object, object)

    typerAdded = QtCore.pyqtSignal(object)
    viewerAdded = QtCore.pyqtSignal(object)
    modelLoaded = QtCore.pyqtSignal(object)
    modellerAdded = QtCore.pyqtSignal(object)
    viewIsDrawn=QtCore.pyqtSignal(object)
    viewIsToBeDrawn=QtCore.pyqtSignal(object)
    viewCreated: QtCore.pyqtSignal = QtCore.pyqtSignal(object)
    viewClosed: QtCore.pyqtSignal = QtCore.pyqtSignal(object)

    def setup(self) -> None:
        super().setup()
        self.setParent(self.app)
        self.app.appViewIsLaunched.connect(self.checkParser)

    def saveView(self, view: tp.Any) -> None:
        super().saveView(view)
        if view:
            view.closeWanted.connect(self.removeView)

    def removeView(self, view=None, **kwargs):
        super().removeView(view=view, **kwargs)
        if view:
            self.viewClosed.emit(view)

    def createViewClass(self, klass, **kwargs):
        view = super().createViewClass(klass, **kwargs)
        self.viewCreated.emit(view)
        return view

    def addView(self, view):
        signal = view.getAttr("posIndexChanged")
        if signal:
            signal.connect(self.posIndexChanged)
        self.viewAdded.emit(view)

    def addViewer(self, name: str, klass: tp.Any) -> tp.Any:
        cond = not klass in self.m_viewers
        super().addViewer(name, klass)
        if cond:
            self.viewerAdded.emit(klass)
        return klass

    def addModeller(self, name: str, klass: tp.Any) -> tp.Any:
        cond = not klass in self.m_modellers
        super().addModeller(name, klass)
        if cond:
            self.modellerAdded.emit(klass)
        return klass

    def createModel(self, *args, **kwargs):
        model = super().createModel(*args, **kwargs)
        if model:
            self.modelCreated.emit(model)
        return model
