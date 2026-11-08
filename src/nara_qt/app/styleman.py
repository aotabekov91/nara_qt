from PyQt6 import QtCore

import nara

class Styleman(nara.Styleman, QtCore.QObject):

    styleChanged=QtCore.pyqtSignal(object)

    def setup(self) -> None:
        super().setup()
        self.setParent(self.app)
        self.app.appSoonStarts.connect(
            self.updateDefault)
