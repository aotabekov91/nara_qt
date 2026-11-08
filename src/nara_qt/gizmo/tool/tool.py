from PyQt6 import QtWidgets

from nara_qt import vimo


class ToolView(
        vimo.View, 
        QtWidgets.QToolBar
):
    pass


    # def setup():
    #     super().setup()
    #     l=self.layout()
    #     self.setContentsMargins(0,0,0,0)
    #     l.setContentsMargins(0,0,0,0)
    #     self.setFloatable(False)
    #     self.setMovable(False)
    #     l.setSpacing(0)
