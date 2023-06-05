import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
import easygui
import threading

# Load script(s)
from src.SCRIPTS import script_compiler as s_compiler

class MainApp(QMainWindow, QWidget):
    signal_back = pyqtSignal(str)

    def __init__(self, ui_file, decomp_or_comp, key):
        super().__init__()
        uic.loadUi(ui_file, self)  # ui file load
        #self.setWindowIcon()  # Icon Loading
        self.v = decomp_or_comp
        self.base_k = key

        self.btn_file_browse.clicked.connect(self._file_browse)
        self.chb_backup.stateChanged.connect(self._change_line_state)
        self.pushButton.clicked.connect(self._startTHREAD)
        self.btn_back.clicked.connect(self._go_back)

        # Changing text
        self.__change_text(self.v)

        # Interaction list (to deactivate them, when (de)compiling)
        self.interaction_list = [
            self.line_file_path,
            self.line_orig_path,
            self.btn_file_browse,
            self.pushButton,
            self.chb_backup
        ]

    def _go_back(self):
        self.signal_back.emit('back')
        self.close()

    def __change_text(self, v):
        if v == 0:
            self.pushButton.setText('Compile')
            self.setWindowTitle('Compile Menu')
            self.label_head.setText('Compile Menu')
        else:
            self.pushButton.setText('Decompile')
            self.setWindowTitle('Decompile Menu')
            self.label_head.setText('Decompile Menu')

    def __setInteraction(self, bool):
        for item in self.interaction_list:

            if item == self.line_orig_path: # Check if checkbox is checked, then enable
                if self.chb_backup.isChecked():
                    item.setEnabled(bool)
                else:
                    pass
            else:
                item.setEnabled(bool)

    def _file_browse(self):
        path = easygui.fileopenbox('Open a file')
        print(path)

        if path == None:
            return print('No file selected')

        self.line_file_path.setText(path)
        orig_file = s_compiler._replace_file_extension(path, '.backup')
        self.line_orig_path.setText(orig_file)

    
    def _change_line_state(self):
        if self.chb_backup.isChecked():
            self.line_orig_path.setEnabled(True)
        else:
            self.line_orig_path.setEnabled(False)

    def _startTHREAD(self):
        self.__setInteraction(False)

        x = threading.Thread(target=self.start)
        x.start()

    def start(self):
        FILE_PATH = self.line_file_path.text()
        if self.chb_backup.isChecked():
            make_backup = True
        else:
            make_backup = False

        
        if FILE_PATH == "" or FILE_PATH == " ":  # Check if empty
            print('FilePath: Empty')
            return self.__setInteraction(True)
        
        cmp = s_compiler.compiler(self.base_k)

        cmp.compile(FILE_PATH, self.v, make_backup)

        print('Finished')
        return self.__setInteraction(True)


        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp('src/FILE_UI/compiler.ui')
    appMain.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exiting...')