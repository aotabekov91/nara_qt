from PyQt6 import QtCore, QtWidgets

from nara import deleg
from nara_qt import vimo

from .item import ListItem
from ..element import ElementView

class ElementListView(vimo.View, QtWidgets.QListWidget):

    include = {}
    exclude = {}
    widget_map = {}
    widget_class = ElementView
    list_item_class = ListItem
    widgetDataChanged = QtCore.pyqtSignal(object)

    def goToDeleg(self, view=None, action=None, **kwargs):
        if action:
            functor=getattr(view, action, None)
            if functor:
                functor(**kwargs)

    def setup(self):
        super().setup()
        self.setProperties()

    def setProperties(self):
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setResizeMode(
            QtWidgets.QListView.ResizeMode.Adjust)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

    def setCurrentRow(self, row):
        super().setCurrentRow(row)
        self.indexChanged.emit(row + 1)

    def setModel(self, model=None, **kwargs):
        if id(self.m_model) != id(model):
            self.reconnectModel("disconnect")
            # self.cleanUp() #todo
            # self.clear()
            super().setModel(model)
            elems = model.elements()
            for idx, element in elems.items():
                if self.include:
                    for k, l in self.include.items():
                        data = element.data()
                        v = data.get(k)
                        if not v in l:
                            break
                        self.addElement(element)
                else:
                    self.addElement(element)
            self.reconnectModel()
            self.goTo(kind='first')

    def cleanUp(self):
        super().clear()
        model = self.m_model
        if model:
            current_item = self.currentItem()
            # for i in range(m.rowCount()):
            for row in range(model.count()):
                idx = model.index(row, 0)
                item = model.itemFromIndex(idx)
                element=item.element()
                list_item = element.listItem()
                list_item.setHidden(True)
                if current_item == list_item:
                    list_item.m_current_idx = True 

    def getWidgetMap(self, element):
        return self.widget_map

    def addElement(self, element):
        wmap = self.getWidgetMap(element)
        list_item = self.list_item_class()
        list_item.setElement(element)
        widget = self.widget_class(
            view=self, 
            wmap=wmap,
            app=self.app,
            manager=self,
            item=list_item, 
            element=element, 
            )
        self.addItem(list_item)
        self.setItemWidget(list_item, widget)
        self.resized.emit(self)

    def updateElement(self, e):
        for i in range(self.count()):
            i = self.item(i)
            if i.element() == e:
                w = self.itemWidget(i)
                w.updateData()

    def removeElement(self, e):
        for i in range(self.count()):
            item = self.item(i)
            if item.element() == e:
                return self.takeItem(i)

    def selectElement(self, element):
        for row in range(self.count()):
            item = self.item(row)
            if item.element() == element:
                return self.setCurrentItem(item)

    def reconnectModel(self, kind="connect"):
        model = self.m_model
        if model and kind == "connect":
            model.elementAdded.connect(self.addElement)
            model.elementRemoved.connect(self.removeElement)
            model.elementWanted.connect(self.selectElement)
        elif model and kind == "disconnect":
            model.elementAdded.disconnect(self.addElement)
            model.elementRemoved.disconnect(self.removeElement)
            model.elementWanted.disconnect(self.selectElement)

    def sizeHint(self):
        height = 0
        hint = super().sizeHint()
        if self.m_model:
            count = self.m_model.count()
            for row in range(count):
                height += self.sizeHintForRow(row)
            hint.setHeight(height)
        return hint

    @deleg('goTo@(normal)[ElementListView]')
    def goTo(self, kind=None, xrange=None, **kwargs):
        # TODO: sometimes this does not work
        if kind:
            func=getattr(self, kind, None)
            if func:
                func(xrange=xrange, **kwargs)
        elif xrange is None:
            self.last(xrange=xrange, **kwargs)
        else:
            self.setCurrentRow(xrange[-1] - 1)

    def first(self, **kwargs):
        self.goTo(xrange=[1])

    def last(self, **kwargs):
        m = self.m_model
        if self.checkProp("rowCount", m):
            xrange = [m.rowCount()]
        else:
            xrange = [m.count()]
        self.goTo(xrange=xrange)

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
        print(action, arg)
        if not action is None:
            idx = self.moveCursor(
                action,
                QtCore.Qt.KeyboardModifier.NoModifier,
            )
            print('valid', idx.isValid())
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
