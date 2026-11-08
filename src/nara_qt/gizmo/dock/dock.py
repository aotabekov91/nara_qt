from PyQt6 import QtWidgets

from nara_qt.vimo import View

from ..tab import TabView

class DockView(
        View, 
        QtWidgets.QDockWidget
        ):
    def __init__(
        self,
        loc=None,
        min_width=200,
        min_height=200,
        zoom_factor=0.1,
        objectName="DockWidget",
        **kwargs,
    ):
        self.loc = loc
        self.min_w = min_width
        self.min_h = min_height
        self.zfactor = zoom_factor
        super().__init__(objectName=objectName, **kwargs)
        self.createTab()


    @property
    def current(self):
        return self.tab.current

    @property
    def previous(self):
        return self.tab.previous

    def createTab(self):
        tab = TabView(
            parent=self,
            app=self.app,
            manager=self,
            identifier="T",
            attributes=[
                {'key':'has_tabs', 'value':False},
                {'key':'initial_create', 'value':False}],
            )
        self.setWidget(tab)
        self.tab = tab
        tab.show()

    def removeView(self, view, **kwargs):
        self.hide()
        self.tab.removeView(view)

    def betView(self, *args, view=None, **kwargs):
        self.hide()
        self.octivate()

    def addView(self, view, **kwargs):
        view.setMinimumSize(self.min_w, self.min_h)
        self.tab.addView(view)
        view.setManager(self)

    def setView(self, *args, view=None, **kwargs)->None:
        self.activate(dock=self, recursive=True)
        self.tab.setView(*args, view=view, **kwargs)

    def insertView(self, idx=-1, view=None, **kwargs):
        self.tab.insertView(idx, view, **kwargs)

    def zoomTo(self, kind, xrange=[1], **kwargs):
        factor=None
        if self.loc=="L" and kind=="R":
            factor = (1.0 + self.zfactor) ** xrange[-1]
        elif self.loc=="L" and kind=="L":
            factor = (1.0 - self.zfactor) ** xrange[-1]
        elif self.loc=="R" and kind=="L":
            factor = (1.0 + self.zfactor) ** xrange[-1]
        elif self.loc=="R" and kind=="R":
            factor = (1.0 - self.zfactor) ** xrange[-1]
        elif self.loc=="U" and kind=="D":
            factor = (1.0 + self.zfactor) ** xrange[-1]
        elif self.loc=="U" and kind=="U":
            factor = (1.0 - self.zfactor) ** xrange[-1]
        elif self.loc=="D" and kind=="U":
            factor = (1.0 + self.zfactor) ** xrange[-1]
        elif self.loc=="D" and kind=="D":
            factor = (1.0 - self.zfactor) ** xrange[-1]
        if factor:
            size = self.size()
            width, height = size.width(), size.height()
            tab_size = self.current.size()
            if self.loc in ["L", "R"]:
                width = int(tab_size.width() * factor)
                self.setFixedWidth(width)
            else:
                height = int(tab_size.height() * factor)
                self.setFixedHeight(height)
