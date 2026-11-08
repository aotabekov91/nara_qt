from PyQt6 import QtWidgets

class Layout(QtWidgets.QGridLayout):

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.m_parent=parent
        self.m_current=(None, None)
        self.m_previous=(None, None)
        self.setup()

    def setup(self):
        pass

    def setCurrentIndex(self, row, col):
        if row!=self.m_current:
            item=self.itemAtPosition(row, col)
            if item:
                widget=item.widget()
                self.m_previous=self.m_current
                self.m_current=(row, col)
                widget.setFocus()

    def count(self):
        return len(self.m_parent.widgets())

    def currentIndex(self):
        return self.m_current

    def goTo(self, kind=None, xrange=[1], **kwargs):
        if self.m_current[0] is None:
            self.setCurrentIndex(0, 0)
        else:
            idx=None
            row, col = self.currentIndex()
            if kind=='up':
                idx=row-xrange[-1]
                row= 0 if idx<0 else idx
            elif kind=='down':
                idx=row+xrange[-1]
                row = self.rowCount()-1 if idx>=self.rowCount() else idx
            elif kind=='left':
                idx=col-xrange[-1]
                col=0 if idx<0 else idx
            elif kind=='right':
                idx=col+xrange[-1]
                col=self.columnCount()-1 if idx>=self.columnCount() else idx
            elif kind=='last':
                row=self.rowCount()-1
                col=self.columnCount()-1
            elif kind=='first':
                row, col = 0, 0
            else:
                return
            self.setCurrentIndex(row, col)
