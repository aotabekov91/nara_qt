from PyQt6 import QtCore, QtWidgets

from nara import deleg
from nara_qt import vimo

class TabView(vimo.View, QtWidgets.QStackedWidget):

    hasTabs = True
    tab_classes = {}
    canSetView = True
    initial_create = True
    viewAdded = QtCore.pyqtSignal(object)
    viewCreated = QtCore.pyqtSignal(object)
    viewRemoved = QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.current = None
        self.previous = None
        self.setProperties()
        if self.initial_create:
            self.initiate()

    def setProperties(self):
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

    @deleg('flipTo@(normal)[TabView]')
    def flipTo(self, view=None, **kwargs):
        view=view or self.previous
        if view:
            view.activate()

    @deleg('moveTo@(normal)[TabView]')
    def moveTo(self, kind=None, xrange=None, view=None, **kwargs):
        if not view:
            idx = self.currentIndex()
            view = self.widget(idx)
        else:
            idx=getattr(view, 'm_tab_name', 0)
        if kind in ["prev", "left"]:
            xrange = [max(0, idx - 1)]
        elif kind in ["next", "right"]:
            xrange = [min(self.count() - 1, idx + 1)]
        elif xrange:
            xrange[-1] -= 1
        elif xrange is None:
            xrange = [self.count() - 1]
        if xrange and view:
            self.removeView(view)
            self.insertView(idx=xrange[-1], view=view, **kwargs)
            view.activate(**kwargs)

    @deleg('goTo@(normal)[Tabview]')
    def goTo(self, xrange=[], kind=None, **kwargs):
        count=self.count()
        idx = self.currentIndex()
        if kind in ["prev", "left"]:
            delta=1
            if xrange:
                delta=xrange[-1]
            idx-=delta
        elif kind in ["next", "right"]:
            delta=1
            if xrange:
                delta=xrange[-1]
            idx+=delta
        elif kind == "first":
            idx=0
        elif kind == "last" or xrange is None:
            idx = count - 1
        elif not xrange:
            return
        else:
            xrange[-1] -= 1
        if idx<0:
            idx=self.count()-1
        elif idx >=count:
            idx=0
        view = self.widget(idx)
        if view:
            view.activate()

    def create(self, focus=False, **kwargs):
        tab = self.getNewTab(**kwargs)
        if focus and tab:
            self.setView(tab)
            tab.activate()
        return tab

    def child(self, pos, recursive=True):
        if pos.startswith("x") and self.current:
            i = self.current.posIndex()
            pos = pos.replace("x", str(i), 1)
        elif pos.startswith("-1"):
            i = self.count() - 1
            pos = pos.replace("-1", str(i), 1)
        return super().child(pos, recursive)

    def addAndGoToNewTab(self, focus=False, **kwargs):
        return self.create(focus=True, **kwargs)

    def addCopyTab(self, tab=None, **kwargs):
        c = self.getCopyTab(tab, **kwargs)
        if c:
            self.addView(c)
        return c

    def addAndGoToCopyTab(self, tab=None, **kwargs):
        c = self.addCopyTab(tab, **kwargs)
        if c:
            c.activate()
        return c

    def initiate(self):
        view = self.create()
        if view:
            self.setView(view=view, focus=False)

    def getCopyTab(self, tab=None, **kwargs):
        c = tab or self.current
        if c and self.checkProp("canCopy", c):
            copy = c.copy()
            self.viewCreated.emit(copy)
            return copy

    def getNewTab(self, **kwargs):
        view = self.tabGet()
        if view:
            self.addView(view, **kwargs)
        return view

    def tabGet(self, kind="default"):
        klass = self.tab_classes.get(kind)
        if klass and self.app:
            view=self.app.buffman.createViewClass(
                    klass=klass, 
                    parent=self, 
                    app=self.app, 
                    pindex=self.m_id, 
                    config=self.m_config,
                    )
            self.viewCreated.emit(view)
            return view
        elif klass:
            view = klass(
                parent=self,
                app=self.app,
                pindex=self.m_id,
                config=self.m_config,
            )
            self.viewCreated.emit(view)
            return view

    def tabAdd(self, tab, **kwargs):
        idx = self.addWidget(tab)
        tab.setPosIndex(idx + 1)
        tab.m_tab_name = idx

    def addView(self, view, **kwargs):
        self.tabAdd(view, **kwargs)
        view.setManager(self)
        self.viewAdded.emit(view)
        self.updateIndex()
        return view

    def setView(self, view=None, recursive_activate=False, **kwargs):
        if view:
            self.previous=self.current
            self.current=view
            self.setCurrentIndex(view.posIndex() - 1)
            if not self.activated and recursive_activate:
                self.activate(recursive_activate=True, **kwargs)

    def insertView(self, idx=-1, view=None, **kwargs):
        super().insertWidget(idx, view)
        idx += 1
        view.setPosIndex(idx)
        view.setManager(self)
        view.m_tab_name = idx
        self.viewAdded.emit(view)
        self.updateIndex()
        return view

    def removeView(self, view, **kwargs):
        super().removeWidget(view)
        idx = view.posIndex()
        self.updateIndex()
        view.setManager()
        view.setPosIndex()
        self.viewRemoved.emit(view)
        return view, idx

    @deleg('close@(normal)[Tabview]')
    def close(self, view=None, limit=1, **kwargs):
        if self.count() <= limit:
            return
        view = view or self.current
        if view:
            self.goTo(kind='prev')
            self.removeView(view)
            view.closeWanted.emit(view)

    def updateIndex(self):
        for i in range(self.count()):
            v = self.widget(i)
            v.setPosIndex(i + 1)

    def activate(self, descend=True, **kwargs):
        super().activate(**kwargs)
        if self.current and descend:
            self.current.activate()
