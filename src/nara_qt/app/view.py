import typing as tp

from PyQt6 import QtCore

from nara_qt import gizmo

class View(gizmo.WindowView):

    activated: bool = True
    isAppView: bool = True
    windowResized: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def __init__(self, app: tp.Any = None, **kwargs) -> None:
        super().__init__(app=app, **kwargs)
        self.setPosIndex(0)

    def setup(self) -> None:
        super().setup()
        self.app.view = self
        self.setupUI()
        self.app.appIsLaunched.connect(
                self.addToBuffer)

    def setupUI(self) -> None:
        self.main: gizmo.TabView = gizmo.TabView(
            label="C",
            parent=self,
            app=self.app,
            manager=self,
            name='Center',
            identifier="C",
            attributes=[{
                'key':'tab_classes',
                'value': {"default": gizmo.TileView},
                'copy': True,
                'kind': 'update',
                }]
            )
        self.docks: gizmo.Docks = gizmo.Docks(
            label="D",
            parent=self,
            app=self.app,
            manager=self,
            identifier="D")
        self.bar: gizmo.StatusBarView = gizmo.StatusBarView(
            label="S",
            parent=self,
            app=self.app,
            manager=self,
            identifier="S",
            name='Statusbar')
        self.setContentsMargins(0, 0, 0, 0)
        self.main.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.main)
        self.setStatusBar(self.bar)
        self.main.resized.connect(
                self.resized)

    def addToBuffer(self) -> None:
        self.app.buffman.addView(self.bar)
        self.app.buffman.addView(self.main)
        self.app.buffman.addView(self.docks)
        current = self.main.current
        if current:
            self.app.buffman.addView(current)

    def addView(self, *args, **kwargs):
        self.main.addView(*args, **kwargs)

    def setView(self, *args, **kwargs):
        self.main.setView(*args, **kwargs)
