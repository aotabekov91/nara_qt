from PyQt6 import QtCore

import nara

class Stateman(
    nara.Stateman,
    QtCore.QObject,
):

    viewChanged = QtCore.pyqtSignal(object)
    modeChanged = QtCore.pyqtSignal(object)
    subviewChanged = QtCore.pyqtSignal(object)
    submodeChanged = QtCore.pyqtSignal(object)

    def setMode(self, *args, **kwargs) -> str:
        mode=self.mode()
        super().setMode(*args, **kwargs)
        if mode!=self.mode():
            self.modeChanged.emit(self.m_mode)
        return self.m_mode

    def setSubmode(self, *args, **kwargs) -> str:
        submode=self.submode()
        super().setSubmode(*args, **kwargs)
        if submode!=self.submode():
            self.submodeChanged.emit(self.m_submode)
        return self.m_submode

    def setView(self, *args, **kwargs):
        view=self.view()
        super().setView(*args, **kwargs)
        if view!=self.view():
            self.viewChanged.emit(self.view())

    def setSubview(self, *args, **kwargs):
        subview=self.subview()
        super().setSubview(*args, **kwargs)
        if subview!=self.subview():
            self.subviewChanged.emit(self.subview())
