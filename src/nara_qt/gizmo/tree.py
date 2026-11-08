from PyQt6 import QtCore, QtWidgets

from nara_qt import vimo

class TreeViewWidget(QtWidgets.QTreeView):

    # itemChanged = QtCore.pyqtSignal(object)

    # todo it does not work here with a separate TreeView 
    # (see the following class)
    # def setModel(self, model):
    #     if model:
    #         super(Tree, self).setModel(model)
    #         super(TreeView, self).setModel(model)

    def count(self, idx=None):
        if self.m_model:
            idx=idx or self.currentIndex()
            pidx=idx.parent()
            if pidx.isValid():
                return self.m_model.rowCount(pidx)
            return self.m_model.rowCount()
        return 0

    def expand(self, idx=None, select=True, **kwargs):
        idx = idx or self.currentIndex()
        super().expand(idx)
        if select:
            self.setCurrentIndex(idx)

    def expandAll(self, idx=None, **kwargs):
        idx = idx or self.currentIndex()
        self.expandRecursively(idx)

    def collapse(self, idx=None, **kwargs):
        idx = idx or self.currentIndex()
        super().collapse(idx)

    def collapseAll(self, item=None, **kwargs):
        item = item or self.currentItem()
        if item:
            super().collapse(item.index())
            for i in range(item.rowCount()):
                self.collapseAll(item.child(i))

    def rootDown(self, xrange=[1], **kwargs):
        model=self.model()
        for row in range(xrange[-1]):
            idx = self.currentIndex()
            if idx and model:
                self.setRootIndex(idx)
                child=model.index(0, 0, idx)
                self.setCurrentIndex(child)

    def rootUp(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            idx = self.rootIndex()
            parent = idx.parent()
            if parent.isValid():
                self.setRootIndex(parent)
                self.setCurrentIndex(idx)

    def parentUp(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            idx = self.currentIndex()
            pidx = idx.parent()
            if pidx.isValid():
                self.setCurrentIndex(pidx)
            else:
                nidx = self.m_model.index(0, 0, pidx)
                self.setCurrentIndex(nidx)

    def parentDown(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            idx = self.currentIndex()
            nidx = self.m_model.index(0, 0, idx)
            if nidx.isValid():
                self.setCurrentIndex(nidx)

    def first(self, **kwargs):
        kwargs['xrange']=[1]
        self.goTo(**kwargs)

    def last(self, **kwargs):
        index = self.currentIndex()
        if index:
            parent = index.parent()
            last_row = index.model().rowCount(parent) - 1
            last = self.m_model.index(last_row, 0, parent)
            self.setCurrentIndex(last)

    def right(self, **kwargs):
        self.expand()

    def left(self, **kwargs):
        self.collapse()

    def up(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            self.move("MoveUp")

    def down(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            self.move("MoveDown")

    def goTo(self, kind=None, xrange=None, **kwargs):
        if kind:
            func=getattr(self, kind, None)
            if func:
                func(xrange=xrange, **kwargs)
        elif xrange is None:
            self.last(xrange=xrange, **kwargs)
        else:
            idx = self.currentIndex()
            parent = idx.parent()
            row = xrange[-1] - 1
            if not parent.isValid():
                parent=QtCore.QModelIndex()
            child = self.m_model.index(row, 0, parent)
            self.setCurrentIndex(child)

    def siblingGoTo(self, xrange=[1], kind="up", **kwargs):
        idx = self.currentIndex()
        if idx:
            pidx = idx.parent()
            if pidx:
                if kind == "up":
                    sidx = idx.row() - xrange[-1] 
                elif kind == "down":
                    sidx = idx.row() + xrange[-1] 
                if pidx.isValid():
                    nidx = self.m_model.index(sidx, 0, pidx)
                else:
                    nidx = self.m_model.index(sidx, 0, pidx)
                self.setCurrentIndex(nidx)

    def move(self, arg, **kwargs):
        cursor=QtWidgets.QAbstractItemView.CursorAction
        action = getattr(cursor, arg, None)
        if not action is None:
            mode=QtCore.Qt.KeyboardModifier.NoModifier
            hint=QtWidgets.QAbstractItemView.ScrollHint
            ensure=hint.EnsureVisible
            idx = self.moveCursor(action, mode)
            self.setCurrentIndex(idx)
            self.scrollTo(idx, ensure) 

    def setCurrentIndex(self, idx):
        if idx and idx.isValid():
            super().setCurrentIndex(idx)
            self.indexChanged.emit(idx)

    def currentItem(self, idx=None):
        model = self.model()
        if model:
            idx = idx or self.currentIndex()
            if type(model) == QtCore.QSortFilterProxyModel:
                idx = model.mapToSource(idx)
            if idx and hasattr(model, "itemFromIndex"):
                return model.itemFromIndex(idx)

class TreeView(vimo.View, TreeViewWidget):

    def setModel(self, model):
        if model:
            super().setModel(model)
            super(TreeViewWidget, self).setModel(model)

    def setup(self):
        super().setup()
        self.setProperties()

    def setProperties(self):
        self.setHeaderHidden(True)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
