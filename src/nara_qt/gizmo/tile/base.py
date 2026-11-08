from PyQt6 import QtWidgets

import typing as tp

from nara import deleg
from nara_qt import vimo

from .layout import TileLayout

class TileView(
        vimo.View,
        QtWidgets.QWidget,
        ):

    canCopy=True
    name='TileView'
    suffix_separator: str = "."
    layout_class: tp.Any = TileLayout
    prefix_keys: tp.List[str] = ["<c-w>(normal)"]

    @deleg('close@(normal)[TileView]')
    def close(self, **kwargs):
        return self.m_layout.close(**kwargs)

    @deleg('goTo@(normal)[TileView]')
    def goTo(self, **kwargs):
        leaf=self.m_layout.goTo(**kwargs)
        if leaf and leaf.view:
            leaf.view.activate(subview=leaf.view)
        return leaf

    @deleg('zoomTo@(normal)[TileView]')
    def zoomTo(self, **kwargs):
        return self.m_layout.zoomTo(**kwargs)

    @deleg('moveTo@(normal)[TileView]')
    def moveTo(self, **kwargs):
        return self.m_layout.moveTo(**kwargs)

    @deleg('flipTo@(normal)[TileView]')
    def flipTo(self, **kwargs):
        self.m_layout.flipTo(**kwargs)

    @deleg('splitTo@(normal)[TileView]')
    def splitTo(
        self,
        view=None,
        focus=True,
        kind="vertical",
        **kwargs,
    ):
        if self.app:
            view = view or self.current
            copy=self.app.delegman.delegate(
                    mode='normal', 
                    view=view, 
                    action='clone', 
                    data={'obj': view})
            if copy:
                orientation = kind == "horizontal"
                print(orientation, kind)
                self.addView(copy, horizontal=orientation)
                if focus:
                    copy.activate(subview=copy)
                    print(copy, self.app.stateman.subview())

    def horizontal(self, view):
        return self.m_layout.horizontal(view)

    def getLeaf(self, view):
        return self.m_layout.getLeaf(view)

    def child(self, pos, recursive=True):
        if pos.startswith("x") and self.current:
            i = self.current.posIndex()
            pos = pos.replace("x", str(i), 1)
        elif pos.startswith("-1"):
            i = self.count() - 1
            pos = pos.replace("-1", str(i), 1)
        return super().child(pos, recursive)

    def setConfig(self):
        if self.app:
            c = self.app.m_config.get("WidgetTileView", {})
            c.update(self.m_config)
            self.m_config = c

    def setParent(self, parent):
        super().setParent(parent)
        if parent and hasattr(parent, "resized"):
            parent.resized.connect(self.update)

    def setup(self):
        self.setConfig()
        super().setup()
        self.setContentsMargins(0, 0, 0, 0)
        self.m_layout = self.layout_class(self)
        self.m_layout.geometryChanged.connect(
            self.geometryChanged
        )

    def focus(self, increment=1):
        if self.m_layout.count() < 2:
            view = self.currentView()
            if view:
                view.setFocus()
        else:
            current = self.currentView()
            idx = self.indexOf(current)
            idx += increment
            if idx >= self.m_layout.count():
                idx = 0
            elif idx < 0:
                idx = self.m_layout.count() - 1
            view = self.widget(idx)
            if view:
                view.activate(subview=view)

    def clear(self):
        self.m_layout.clear()

    def addView(self, view=None, **kwargs):
        if view:
            view.setManager(self)
            self.m_layout.addView(view=view, **kwargs)
            return view

    def insertView(self, idx, view, **kwargs):
        view.setManager(self)
        return self.m_layout.insertView(idx, view, **kwargs)

    def setView(self, *args, **kwargs):
        self.m_layout.setView(*args, **kwargs)

    def removeView(self, view=None, **kwargs):
        if not view:
            leaf = self.m_layout.current_leaf
            if leaf: 
                view = leaf.view
        if view:
            return self.m_layout.removeView(view)

    def update(self):
        self.m_layout.update()

    def count(self):
        return self.m_layout.count()

    @property
    def current(self):
        return self.m_layout.current

    @property
    def previous(self):
        return self.m_layout.previous

    def activate(self, descend=True, **kwargs):
        super().activate(**kwargs)
        if self.current and descend:
            self.current.activate()
