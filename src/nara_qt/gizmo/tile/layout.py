from PyQt6 import QtCore

from .leaf import TileLeaf

class TileLayout(QtCore.QObject):

    geometryChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        self.delta = 10
        self.ratio = 1.6
        self.m_count = 0
        self.parent = parent
        self.lower_right = True
        self.root = TileLeaf()
        self.current = None
        self.previous = None
        self.previous_leaf = None
        self.current_leaf = self.root
        super().__init__(parent)

    def setSpacing(self, v):
        pass  # todo

    def setContentsMargins(self, l, t, r, b):
        pass  # todo

    def clear(self):
        for view in self.root.views():
            self.removeView(view=view)

    def count(self):
        return self.m_count

    def views(self):
        return self.root.views()

    def horizontal(self, view):
        leaf=self.getLeaf(view)
        if leaf:
            return leaf.horizontal

    def getLeaf(self, view):
        if not view:
            return
        for leaf in self.root:
            if view is leaf.view:
                return leaf

    def setLeaf(self, leaf):
        if not leaf is None:
            current, previous = leaf, self.current_leaf
            self.current_leaf=current
            self.previous_leaf=previous

    def setView(self, *args, view=None, **kwargs):
        if view:
            current, previous = view, self.current
            if current!=previous:
                self.current, self.previous = current, previous
            leaf = self.getLeaf(view)
            self.setLeaf(leaf)
            self.update()
            return leaf

    def insertView(
            self, idx, view, horizontal=True, **kwargs):
        view.setParent(self.parent)
        if self.count() == 0:
            return self.addView(
                view=view, horizontal=horizontal, **kwargs
            )
        else:
            leaf = self.root
            for aview in self.views():
                if aview.posIndex() == idx:
                    leaf = self.getLeaf(aview)
                    break
            leaf.horizontal = horizontal
            leaf.insert(view, 0, self.ratio)
        self.update()
        self.m_count += 1
        self.setView(view)

    def addView(
        self,
        view=None,
        horizontal=True,
        **kwargs,
    ):
        if view:
            view.setParent(self.parent)
            self.current_leaf = (
                self.current_leaf or self.root
            )
            leaf = self.current_leaf
            leaf.horizontal = horizontal
            leaf.insert(
                view,
                int(self.lower_right),
                self.ratio,
            )
            self.m_count += 1
            if not self.current:
                self.setView(view)

    def removeView(self, view=None, **kwargs):
        view = view or self.current
        view.setManager()
        view.setParent(None)
        leaf = self.getLeaf(view)
        if leaf:
            parent_leaf = leaf.m_parent
            if parent_leaf:
                ort = parent_leaf.horizontal
                idx = parent_leaf.leaves.index(leaf)
                leaf = leaf.m_parent.remove(leaf)
                next_view = next(leaf.views(), None)
                if next_view is None:
                    self.current_leaf = self.root
                else:
                    self.setView(next_view)
                if leaf.m_parent:
                    leaf.m_parent.update()
                else:
                    self.root.update()
                return next_view, (idx, ort, parent_leaf)
            leaf.view = None
            self.current_leaf = self.root
        self.m_count -= 1
        return None, None

    def update(self):
        r = self.parent.rect()
        x, y = r.x(), r.y()
        w, h = r.width(), r.height()
        self.root.calc_geom(x, y, w, h)
        self.geometryChanged.emit()

    def toggleSplit(self):
        if self.current_leaf.m_parent:
            cond = self.current_leaf.m_parent.horizontal
            self.current_leaf.m_parent.horizontal = not cond
            self.update()

    def findSibling(self, v=None, kind="next"):
        view = v or self.current_leaf.view
        views = list(self.root.views())
        i = views.index(view)
        if kind == "next":
            idx = min(len(views) - 1, i + 1)
        elif kind == "prev":
            idx = max(0, i - 1)
        if views:
            return views[idx]

    def findLeaf(self, kind):
        leaf = self.current_leaf
        parent = leaf.m_parent
        while parent:
            x, y = (
                self.current_leaf.x,
                self.current_leaf.y,
            )
            w, h = (
                self.current_leaf.w,
                self.current_leaf.h,
            )
            if kind == "up":
                if parent.horizontal and leaf is parent.leaves[1]:
                    n_ = parent.leaves[0]
                    center = x + w * 0.5
                    while n_.view is None:
                        c = n_.leaves[1].x < center
                        if not n_.horizontal or c:
                            n_ = n_.leaves[1]
                        else:
                            n_ = n_.leaves[0]
                    return n_
            elif kind == "down":
                if parent.horizontal and leaf is parent.leaves[0]:
                    n_ = parent.leaves[1]
                    center = x + w * 0.5
                    while n_.view is None:
                        c = n_.leaves[1].x > center
                        # if not n_.horizontal or c: # BUGFIX?
                        if n_.horizontal or c:
                            n_ = n_.leaves[0]
                        else:
                            n_ = n_.leaves[1]
                    return n_
            elif kind == "left":
                if not parent.horizontal and leaf is parent.leaves[1]:
                    n_ = parent.leaves[0]
                    center = y + h * 0.5
                    while n_.view is None:
                        c = n_.leaves[1].y < center
                        if n_.horizontal or c:
                            n_ = n_.leaves[1]
                        else:
                            n_ = n_.leaves[0]
                    return n_
            elif kind == "right":
                if not parent.horizontal and leaf is parent.leaves[0]:
                    n_ = parent.leaves[1]
                    center = y + h * 0.5
                    while n_.view is None:
                        c = n_.leaves[1].y > center
                        if n_.horizontal or c:
                            n_ = n_.leaves[0]
                        else:
                            n_ = n_.leaves[1]
                    return n_
            leaf = parent
            parent = leaf.m_parent

    def equalizeSize(self):
        cond = False
        for leaf in self.root:
            if leaf.ratio != 50:
                leaf.ratio = 50
                cond = True
        if cond:
            self.root.equalize()
            self.update()

    def goTo(self, kind=None, xrange=None, view=None, **kwargs):
        view = view or self.current_leaf.view
        pos = ["right", "left", "down", "up"]
        if kind in pos:
            leaf = self.findLeaf(kind)
            self.setLeaf(leaf)
            return leaf
        elif kind == "next":
            next_view = self.findSibling(view, "next")
            return self.setView(view=next_view)
        elif kind == "prev":
            next_view = self.findSibling(view, "prev")
            return self.setView(view=next_view)
        elif kind == "first":
            next_view = next(self.root.views(), None)
            return self.setView(view=next_view)
        elif kind == "last":
            views = list(self.root.views())
            next_view = views[-1] if len(views) else None
            print(next_view, self.current)
            # TODO: does not jump to the last tile here
            # TEMPYSOL: Without it the current view is not activated
            if next_view:
                next_view.activate()
            return self.setView(next_view)
        elif type(xrange[-1]) == int:
            idx=xrange[-1]-1
            views = list(self.root.views())
            if 0 <= idx < len(views):
                next_view = views[idx]
                return self.setView(view=next_view)

    def moveTo(
        self,
        xrange=[1],
        kind=None,
        view=None,
        **kwargs,
    ):
        view = view or self.current_leaf.view
        cleaf = self.getLeaf(view)
        if kind:
            nleaf = self.findLeaf(kind)
            if nleaf and cleaf:
                self.flipTo(nleaf.view, cleaf.view, focus=False)
            else:
                if self.count()>1:
                    cleaf = self.current_leaf
                    self.removeView(view=cleaf.view)
                    newroot = TileLeaf()
                    if kind in ["up", "down"]:
                        newroot.horizontal = True
                    elif kind in ["left", "right"]:
                        newroot.horizontal = False
                    if kind in ["up", "left"]:
                        newroot.leaves = [
                            cleaf,
                            self.root,
                        ]
                    elif kind in ["down", "right"]:
                        newroot.leaves = [
                            self.root,
                            cleaf,
                        ]
                    self.root.m_parent = newroot
                    cleaf.m_parent = newroot
                    self.root = newroot
                    if cleaf.view:
                        cleaf.view.setManager(self.parent)
                        cleaf.view.setParent(self.parent)
                        cleaf.view.activate()
        else:
            xrange = xrange or self.count()
            xrange[-1] -= 1
            views = list(self.root.views())
            if 0 <= xrange < len(views):
                v = views[xrange]
                nleaf = self.getLeaf(v)
                self.flipTo(nleaf, cleaf)

    def flipTo(self, new=None, old=None, focus=True, **kwargs):
        old=old or self.current
        new=new or self.previous
        new_leaf=self.getLeaf(old)
        current_leaf=self.getLeaf(new)
        nparent = getattr(new_leaf, "m_parent", None)
        cparent = getattr(current_leaf, "m_parent", None)
        if cparent and nparent:
            if focus:
                new.activate()
            cidx = cparent.leaves.index(current_leaf)
            nidx = nparent.leaves.index(new_leaf)
            cparent.leaves[cidx] = new_leaf
            nparent.leaves[nidx] = current_leaf
            new_leaf.m_parent = cparent
            current_leaf.m_parent = nparent
            self.update()
        return new_leaf, current_leaf

    def zoomTo(self, kind=None, inc=True, xrange=[1]):
        leaf = self.current_leaf
        parent = leaf.m_parent
        delta = self.delta * xrange[-1]
        while parent:
            cond = parent.horizontal
            if kind=='equal':
                return self.equalizeSize()
            if kind in ["left", "right"]:
                cond = not parent.horizontal
            if kind in ["right", "down"]:
                cond = cond and leaf is parent.leaves[0]
                ratio = max(5, parent.ratio - delta)
                if inc:
                    ratio = min(95, parent.ratio + delta)
            elif kind in ["left", "up"]:
                cond = cond and leaf is parent.leaves[1]
                ratio = min(95, parent.ratio + delta)
                if inc:
                    ratio = max(5, parent.ratio - delta)
            if cond:
                parent.ratio = ratio
                parent.update()
                break
            leaf = parent
            parent = leaf.m_parent

    def close(self, view=None, **kwargs):
        view = view or self.current
        if view:
            prev_view = self.findSibling(kind="prev")
            next_view = self.findSibling(kind="next")
            view.octivate()
            if prev_view and view != prev_view:
                self.m_count-=1
                self.removeView(view=view)
                prev_view.activate()
                return prev_view
            elif next_view and view!=next_view:
                self.m_count-=1
                self.removeView(view=view)
                next_view.activate()
                return next_view
            else:
                # TODO: this message should be rendered via Message plugin
                print('Cannot close the last view')
