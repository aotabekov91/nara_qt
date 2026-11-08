import os
import sys
import time
import tomli
import typing as tp

from PyQt6 import QtCore, QtWidgets

import nara

from .view import View
from .earman import Earman
from .buffman import Buffman
from .plugman import Plugman
from .styleman import Styleman
from .stateman import Stateman
from .configman import Configman


class App(nara.App, QtCore.QObject):

    appSoonQuits: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appIsLaunched: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appSoonStarts: QtCore.pyqtSignal = QtCore.pyqtSignal()
    appViewIsLaunched: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def setupApp(self):
         self.setupParser()
         self.setupQApp()
         self.setupParts()
         self.setupView()

    def setupQApp(self) -> None:
         self.qapp: QtWidgets.QApplication = (
             QtWidgets.QApplication(sys.argv)
         )
         self.qapp.setApplicationName(self.name)
         self.setParent(self.qapp)
    
    def setupView(self, klass: tp.Any = View) -> None:
         if klass:
             self.ui = klass(app=self)
    
    def setupParts(
         self,
         plugman = Plugman,
         earman = Earman,
         buffman = Buffman,
         styleman = Styleman,
         stateman = Stateman,
         configman = Configman,
     ) -> None:
         super().setupParts(
                 plugman=plugman,
                 earman=earman,
                 buffman=buffman,
                 styleman=styleman,
                 configman=configman,
                 stateman=stateman)

    def run(self) -> None:
         self.appSoonStarts.emit()
         self.startView()
         self.appViewIsLaunched.emit()
         self.running=True
         self.appIsLaunched.emit()
         sys.exit(self.qapp.exec())
