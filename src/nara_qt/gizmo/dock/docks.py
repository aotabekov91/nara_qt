from PyQt6 import QtCore, QtWidgets

from nara_qt.vimo import View

from .dock import DockView


class Docks(
    View,
    QtCore.QObject,
):

    number_mapping={1:'L', 2:'U', 3:'R', 4:'D'}

    def setup(self):
        super().setup()
        self.m_docks = []
        self.current = None
        self.previous=None
        self.createDocks()

    def createDocks(self):
        parent=self.parent()
        parent.setCorner(
            QtCore.Qt.Corner.TopLeftCorner,
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
        )
        parent.setCorner(
            QtCore.Qt.Corner.TopRightCorner,
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
        )
        parent.setCorner(
            QtCore.Qt.Corner.BottomLeftCorner,
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
        )
        parent.setCorner(
            QtCore.Qt.Corner.BottomRightCorner,
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
        )
        locs = {
            "left": QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
            "up": QtCore.Qt.DockWidgetArea.TopDockWidgetArea,
            "right": QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
            "down": QtCore.Qt.DockWidgetArea.BottomDockWidgetArea,
        }
        for i, (loc, r) in enumerate(locs.items()):
            loc = loc[0].upper()
            dock = DockView(
                loc=loc,
                label=loc,
                pindex=i + 1,
                app=self.app,
                manager=self,
                identifier=loc,
            )
            dock.setContentsMargins(0, 0, 0, 0)
            dock.title = QtWidgets.QWidget()
            dock.setTitleBarWidget(dock.title)
            parent.addDockWidget(r, dock)
            setattr(self, f"{loc}", dock)
            self.m_docks += [dock]
        self.hide(kind='all')

    def moveTo(self, kind=None, dock=None, view=None, **kwargs):
        dock = getattr(self, kind, None)
        if not view and self.current:
            view=self.current.current
        if view:
            self.addView(view=view, dock=dock, **kwargs)
            view.activate(**kwargs)

    def goTo(self, kind=None, **kwargs):
        dock = getattr(self, kind, None)
        if dock and dock.current:
            dock.current.activate(**kwargs)

    def flipTo(self, new_view=None, old_view=None, focus=False, **kwargs):
        if not new_view and self.previous:
            new_view=self.previous.current
        if not old_view and self.current:
            old_view=self.current.current
        if new_view and old_view:
            self.addView(view=new_view, dock=self.current)
            self.addView(view=old_view, dock=self.previous)
            old_view.activate()
            new_view.activate()
            if focus:
                old_view.activate()

    def activate(self, dock=None, **kwargs):
        self.setCurrentDock(dock=dock)

    def zoomTo(self, dock=None, **kwargs):
        dock = dock or self.current
        if dock:
            dock.zoomTo(**kwargs)

    def hide(self, xrange=[], kind=None, **kwargs):
        if kind=='all':
            for dock in self.m_docks: 
                dock.hide()
                dock.octivate(**kwargs)
        elif xrange:
            idx=xrange[-1]
            loc=self.number_mapping.get(idx, None)
            dock = getattr(self, loc, None)
            if dock:
                dock.hide()
                dock.octivate(**kwargs)
        elif self.current:
            self.current.hide()
            self.current.octivate(**kwargs)

    def addView(self, view=None, loc=None, dock=None, **kwargs):
        if not dock and loc:
            dock = getattr(self, loc, None)
        if dock and view:
            self.removeView(view=view)
            dock.addView(view=view)
            return dock

    def removeView(self, view=None, **kwargs):
        if view:
            manager=view.manager()
            if manager:
                manager.hide()
                manager.removeView(view)
                manager.octivate(**kwargs)
            return view

    def setCurrentDock(self, dock=None):
        if dock and dock!=self.current:
            self.previous=self.current
        self.current = dock
