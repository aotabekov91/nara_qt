class SinglePage:

    def __init__(
        self,
        config={},
        pageSpacing=0,
        viewportPadding=0,
        **kwargs,
    ):
        self.m_config = config
        self.pageSpacing = pageSpacing
        self.viewportPadding = viewportPadding
        self.setSettings()

    def setSettings(self):
        c = self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def left(self, idx, count=None):
        return idx

    def right(self, idx, count=None):
        return idx

    def up(self, idx, count=None):
        return idx

    def down(self, idx, count=None):
        return idx

    def next(self, idx, count=None):
        return min(idx + 1, count)

    def prev(self, idx, count=None):
        return max(idx - 1, 1)

    def current(self, idx, count=None):
        return idx

    def width(self, width):
        ps = self.pageSpacing
        return width - self.viewportPadding - 2.0 * ps

    def height(self, height):
        return height - 2.0 * self.pageSpacing

    def itemsAt(
        self,
        rect,
        items,
    ):
        for i in items.values():
            if i.m_rect.intersects(rect):
                yield i

    def load(
        self,
        items,
        x,
        right,
        height,
        *args,
        **kwargs,
    ):
        ph = 0.0
        page_spacing = self.pageSpacing
        for item in items.values():
            rect = item.boundingRect()
            x = -rect.left() - 0.5 * rect.width()
            y = height - rect.top()
            w, h = rect.width(), rect.height()
            item.setPos(x, y)
            if hasattr(item, "m_rect"):
                item.m_rect.setX(x)
                item.m_rect.setY(y)
                item.m_rect.setWidth(w)
                item.m_rect.setHeight(h)
            ph = rect.height()
            x = min(x, -0.5 * rect.width())
            right = max(right, 0.5 * rect.width())
            height += page_spacing + ph
        return x, right, height
