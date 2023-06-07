import tomllib

# - Load config
cfg = tomllib.loads(open('src/CONFIG', 'r').read())


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot

# - Importing scripts (for building process, or they won't be able to load correctly)
from src.SCRIPTS import script_compiler as s_compiler
from src.SCRIPTS_UI import ui_compiler
from src.SCRIPTS import script_styler as s_styler
from json import loads as jsn

# - Set style for other windows and main window
if cfg['theme:enabled']:
    themelist = jsn(open(cfg['theme:list'], 'r').read())
    style = s_styler._convert_stylesheet(themelist, cfg['theme:folder'], cfg['theme:defaultindex'])
else:
    style = ''

class MainApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg['ui:main'], self)  # ui file load
        #self.setWindowIcon()  # Icon Loading
        self.decomp_or_comp = -1
        self.key = cfg['default:key']
        self.key = open(self.key, 'rb').read()

        self.btn_compile.clicked.connect(self._set_compile)
        self.btn_decompile.clicked.connect(self._set_decompile)

    def _set_compile(self):
        self.decomp_or_comp = 0
        self._load_ui(self.decomp_or_comp, self.key)
    
    def _set_decompile(self):
        self.decomp_or_comp = 1
        self._load_ui(self.decomp_or_comp, self.key)

    def _load_ui(self, v, key):
        self.compile_ui = ui_compiler.MainApp(cfg['ui:compiler'], v, key, style)

        self.compile_ui.show()
        self.close()

        self.compile_ui.signal_back.connect(self._show_main)
    
    @pyqtSlot(str)
    def _show_main(self, text):
        self.show()
        

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp()
    appMain.show()

    appMain.setStyleSheet(style)

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('SYSTEM_EXIT')