from PyQt6 import QtGui

def setEditorTabSize(editor, tab_stop):
    fm = QtGui.QFontMetrics(editor.font())
    stop_width = fm.horizontalAdvance(" ") * tab_stop
    editor.setTabStopDistance(int(stop_width))
