from PyQt6 import QtCore

from nara_qt import vimo

from .tool import ToolView


class Tools(vimo.View, QtCore.QObject):
    def __init__(
        self,
        app=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(
            app=app,
            parent=parent,
            **kwargs,
        )

        self.m_tools = []
        self.m_current = None
        self.m_window = parent
        self.createTools()

    def createTools(self):
        locs = {
            "up": QtCore.Qt.TopToolBarArea,
            "left": QtCore.Qt.LeftToolBarArea,
            "down": QtCore.Qt.BottomToolBarArea,
            "right": QtCore.Qt.RightToolBarArea,
        }

        for loc, r in locs.items():
            d = ToolView(app=self.app)
            self.m_window.addToolBar(r, d)
            setattr(self, f"{loc}", d)
            self.m_tools += [d]
            d.hide()
