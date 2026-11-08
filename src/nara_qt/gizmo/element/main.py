from collections import OrderedDict

from PyQt6 import QtCore, QtWidgets

from nara_qt.vimo import View

from . import widgets
from .layout import Layout

class ElementView(View, QtWidgets.QWidget):

    wmap = {
        "Label": widgets.Label,
        "Image": widgets.Image,
        "LineEdit": widgets.LineEdit,
        "TextEdit": widgets.TextEdit,
    }
    widget_map = {}
    hasWidgets = True
    dataChanged = QtCore.pyqtSignal(object, object)

    def __init__(
        self,
        wmap={},
        space=0,
        hspace=0,
        vspace=0,
        item=None,
        view=None,
        element=None,
        objectName="ItemWidget",
        **kwargs,
    ):
        self.m_view = view
        self.m_item = item
        self.m_space = space
        self.m_element = None
        self.m_vspace = vspace
        self.m_hspace = hspace
        self.m_wmap = wmap.copy()
        self.m_widgets = OrderedDict()
        super().__init__(objectName=objectName, **kwargs)
        self.setupLayout()
        self.setView(view)
        self.setElement(element)

    def element(self):
        return self.m_element

    def setupLayout(self):
        layout = Layout(parent=self)
        self.setLayout(layout)
        self.m_layout = layout
        layout.setSpacing(self.m_space)
        layout.setVerticalSpacing(self.m_vspace)
        layout.setHorizontalSpacing(self.m_hspace)

    def setView(self, view):
        self.m_view = view
        self.setParent(view)
        if not view:
            return
        view.resized.connect(self.adjustSizeHint)

    def setElement(self, element=None, widgets=None):
        if self.m_element:
            signal = getattr(
                self.m_element,
                "dataUpdated",
                None,
            )
            if signal:
                signal.dataUpdated.disconnect(self.updateData)
            self.delWidgets(self.m_widgets)
        self.m_element = element
        if self.m_element:
            signal = getattr(
                self.m_element,
                "dataUpdated",
                None,
            )
            if signal:
                signal.dataUpdated.connect(self.updateData)
            if not widgets:
                widgets = self.createWidgets()
            self.setWidgets(widgets)

    def createWidgets(self, element=None, widget_map=None):
        widgets = OrderedDict()
        wmap = widget_map or self.m_wmap
        elem = element or self.m_element
        items = wmap.items()
        data = elem.data()
        for row, (item_idx, item_data) in enumerate(items):
            klass = item_data.get("w", "Label")
            p = item_data.get("p", f"{row}x0x-1x1")
            p = [int(f) for f in p.split("x")]
            text = str(data.get(item_idx, "")).strip()
            text = item_data.get("t", text)
            pos = (p[0], p[1])
            if type(klass) == str:
                klass = self.wmap.get(klass)
            if klass:
                widget = klass(
                    data=item_data,
                    text=text,
                    index=item_idx,
                    parent=self,
                    position=pos,
                    element=self.m_element,
                )
                object_name = item_idx
                widgets[item_idx] = (widget, p)
                field_name = item_data.get("n", None)
                if field_name:
                    field_name = field_name.split("_")
                    item_data = self.m_element.data()
                    field_text = []
                    for field in field_name:
                        field_text += [item_data.get(field, "")]
                    object_name = "_".join(field_text)
                widget.setObjectName(object_name)
        return widgets

    def delWidgets(self, widgets):
        for widget, _ in widgets.values():
            self.m_layout.removeWidget(widget)
            widget.geometryChanged.disconnect(
                self.adjustSizeHint)
            widget.focusGained.disconnect(self.selectToCenter)
            widget.hide()
        self.m_widgets = OrderedDict()

    def setWidgets(self, widgets):
        for w, p in widgets.values():
            self.m_layout.addWidget(w, *p)
            w.focusGained.connect(self.selectToCenter)
            w.geometryChanged.connect(self.adjustSizeHint)
            w.show()
        self.m_widgets = widgets

    def widget(self, key=None, idx=None):
        if key:
            return self.m_widgets.get(key)
        elif idx:
            widgets=self.m_widgets.values()
            for num, data in enumerate(widgets):
                if idx==num+1:
                    return data[0]

    def widgets(self):
        return self.m_widgets

    def updateData(self):
        d = self.m_element.data()
        for n in self.m_widgets.keys():
            self.set(n, str(d[n]).strip())

    def set(self, key, text):
        widget, _ = self.m_widgets[key]
        widget.m_reporting = False
        widget.setText(str(text))
        widget.m_reporting = True

    def sizeHint(self):
        v = self.size()
        hint = super().sizeHint()
        if not self.m_widgets:
            return hint
        h = 10
        for i, p in self.m_widgets.values():
            h += i.sizeHint().height()
        if self.m_view:
            v = self.m_view.size()
        h = max(hint.height(), h)
        hint.setHeight(h)
        hint.setWidth(v.width())
        return hint

    def adjustSizeHint(self):
        if self.m_item:
            self.m_item.setSizeHint(self.sizeHint())

    def selectToCenter(self):
        if self.m_view:
            self.m_view.setCurrentItem(self.m_item)
            self.m_view.scrollToItem(self.m_item)

    def goTo(self, *args, **kwargs):
        return self.m_layout.goTo(*args, **kwargs)

    def currentIndex(self):
        return self.m_layout.currentIndex()

    def setCurrentIndex(self, *args, **kwargs):
        self.m_layout.setCurrentIndex(*args, **kwargs)
