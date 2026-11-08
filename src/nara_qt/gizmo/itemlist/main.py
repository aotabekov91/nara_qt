from PyQt6 import QtCore, QtWidgets

from nara_qt import vimo

class ItemListView(vimo.View, QtWidgets.QListView):

    def setup(self):
        super().setup()
        self.setProperties()

    def setProperties(self):
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def setModel(self, model):
        if model:
            super().setModel(model)
            super(QtWidgets.QListView, self).setModel(model)

    def goTo(self, kind=None, xrange=None, **kwargs):
        if kind:
            func=getattr(self, kind, None)
            if func:
                func(xrange=xrange, **kwargs)
        elif xrange is None:
            self.last(xrange=xrange, **kwargs)
        else:
            idx = self.getRowIndex(xrange[-1] - 1)
            self.setCurrentIndex(idx)

    def first(self, **kwargs):
        self.goTo(xrange=[1])

    def last(self, **kwargs):
        m = self.m_model
        if self.checkProp("rowCount", m):
            xrange = [m.rowCount()]
        else:
            xrange = [m.count()]
        self.goTo(xrange)

    def up(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            self.move("MoveUp")

    def down(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            self.move("MoveDown")

    def move(self, arg):
        action = getattr(
                QtWidgets.QAbstractItemView.CursorAction, 
                arg, 
                None)
        if not action is None:
            idx = self.moveCursor(
                action,
                QtCore.Qt.KeyboardModifier.NoModifier,
            )
            self.setCurrentIndex(idx)
            self.scrollTo(
                    idx, 
                    QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible,
                    )
        else:
            self.goToFirst()

    def getRowIndex(self, row):
        return self.model().index(row, 0)

    def setCurrentIndex(self, idx):
        super().setCurrentIndex(idx)
        if type(idx) == int:
            self.indexChanged.emit(idx)
        else:
            self.indexChanged.emit(idx.row() + 1)
