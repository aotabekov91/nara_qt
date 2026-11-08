from PyQt6 import QtCore


class TileLeaf(QtCore.QObject):

    def __init__(self, parent=None):
        self.ratio = 50
        self.leaves = []
        self.view = None
        self.horizontal = False
        self.m_parent = parent
        self.x, self.y = 0, 0
        self.h, self.w = 9, 16
        super().__init__(parent)

    def parentLeaf(self):
        return self.m_parent

    def __iter__(self):
        yield self
        for leaf in self.leaves:
            for c in leaf:
                yield c

    def views(self):
        if self.view:
            yield self.view
        else:
            for leaf in self.leaves:
                for c in leaf.views():
                    yield c

    def _shortest(self, length):
        if len(self.leaves) == 0:
            return self, length

        leaf0, length0 = self.leaves[0]._shortest(
            length + 1
        )
        leaf1, length1 = self.leaves[1]._shortest(
            length + 1
        )

        if length1 < length0:
            return leaf1, length1
        return leaf0, length0

    def get_shortest(self):
        return self._shortest(0)[0]

    def insert(self, view, idx, ratio):
        if self.view is None:
            self.view = view
            view.m_leaf_idx = idx
            return self

        self.leaves = [
            TileLeaf(self),
            TileLeaf(self),
        ]
        self.leaves[1 - idx].view = self.view
        self.leaves[idx].view = view
        view.m_leaf_idx = idx
        self.view = None
        return self.leaves[idx]

    def remove(self, leaf):
        keep = self.leaves[0]
        if leaf in self.leaves[0]:
            keep = self.leaves[1]
        self.leaves = keep.leaves
        for c in self.leaves:
            c.m_parent = self
        self.horizontal = keep.horizontal
        leaf.view.m_leaf_idx = None
        self.ratio = keep.ratio
        self.view = keep.view
        return self

    def equalize(self):
        if len(self.leaves) == 0:
            return 1, 1
        h0, v0 = self.leaves[0].equalize()
        h1, v1 = self.leaves[1].equalize()
        if self.horizontal:
            h = h0 + h1
            v = max(v0, v1)
            self.ratio = 100 * h0 / h
        else:
            h = max(h0, h1)
            v = v0 + v1
            self.ratio = 100 * v0 / v
        return h, v

    def update(self):
        self.calc_geom(self.x, self.y, self.w, self.h)

    def calc_geom(self, x, y, w, h, idx=0):
        if self.view:
            idx += 1
            self.view.setPosIndex(idx)
        self.x, self.y = x, y
        self.h, self.w = h, w
        if len(self.leaves) > 1:
            leaves = self.leaves
            if not self.horizontal:
                w0 = int(self.ratio * w * 0.01 + 0.5)
                idx = leaves[0].calc_geom(x, y, w0, h, idx)
                idx = leaves[1].calc_geom(
                    x + w0, y, w - w0, h, idx
                )
            else:
                h0 = int(self.ratio * h * 0.01 + 0.5)
                idx = leaves[0].calc_geom(x, y, w, h0, idx)
                idx = leaves[1].calc_geom(
                    x, y + h0, w, h - h0, idx
                )
        if self.view:
            self.view.setGeometry(x, y, w, h)
            self.view.show()
        return idx
