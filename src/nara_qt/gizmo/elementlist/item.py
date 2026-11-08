from PyQt6.QtWidgets import QListWidgetItem

class ListItem(QListWidgetItem):

    # def setCurrentItem(self):
    #     widget = self.listWidget()
    #     widget.setCurrentItem(self)

    def setElement(self, element):
        self.m_elem = element
        if hasattr(element, "elementWanted"):
            element.elementWanted.connect(self.setCurrentItem)

    def element(self):
        return self.m_elem
