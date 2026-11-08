from .single import SinglePage

class Layout:

    def __init__(
        self,
        view,
        mode="SinglePage",
        modes={"SinglePage": SinglePage},
        **kwargs,
    ):
        self.modes = modes
        self.m_mode = modes[mode](**kwargs)

    def mode(self):
        return self.m_mode

    def left(self, idx, count=None):
        return self.m_mode.left(idx, count)

    def right(self, idx, count=None):
        return self.m_mode.right(idx, count)

    def up(self, idx, count=None):
        return self.m_mode.up(idx, count)

    def down(self, idx, count=None):
        return self.m_mode.down(idx, count)

    def width(self, width):
        return self.m_mode.width(width)

    def height(self, height):
        return self.m_mode.height(height)

    def next(self, idx, count=None):
        return self.m_mode.next(idx, count)

    def prev(self, idx, count=None):
        return self.m_mode.prev(idx, count)

    def current(self, idx, count=None):
        return self.m_mode.current(idx, count)

    def itemsAt(
        self,
        rect,
        items,
    ):
        return self.m_mode.itemsAt(rect, items)

    def load(
        self,
        items,
        left=0.0,
        right=0,
        height=0.0,
        rightToLeft=False,
    ):
        height = height or self.m_mode.pageSpacing
        return self.m_mode.load(
            items,
            left,
            right,
            height,
            rightToLeft,
        )
