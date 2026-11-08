import tomli

from PyQt6 import QtCore

import nara

class Configman(nara.Configman, QtCore.QObject):

    appConfigChanged = QtCore.pyqtSignal()

    def setup(self):
        super().setup()
        self.setupWatcher()

    def setupWatcher(self):
        self.watcher=QtCore.QFileSystemWatcher()
        self.setupConfigWatcher()

    def setupConfigWatcher(self):
        config=self.app.files.get('config.toml', None)
        if config:
            self.watcher.addPath(config)
            self.watcher.fileChanged.connect(self.resetConfig)
    
    def resetConfig(self, path) -> None:
        n=0
        while not os.path.exists(path):
            time.sleep(0.5)
            n+=1
            if n>5: return
        with open(path, "rb") as y:
            self.m_config_file = tomli.load(y)
        self.appConfigChanged.emit()
        self.setupConfigWatcher()


