from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os, sys, subprocess
from Resources.interfaz import Ui_Dialog as Ui_MainWindow
from Resources.success import Ui_Dialog as Ui_DoneWindow

class DoneWindow(QtWidgets.QDialog):
    def __init__(self):
        super(DoneWindow, self).__init__()
        self.ui = Ui_DoneWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.pushButton.clicked.connect(self.button_ok)

    def button_ok(self):
        self.accept()
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.w = None
        self.ui.setupUi(self)
        self.file_format = ''
        self.ui.button_only_audio.toggled.connect(self.radio_only_audio)
        self.ui.button_video.toggled.connect(self.radio_video)
        self.ui.push_button_cancel.clicked.connect(self.button_cancel)
        self.ui.push_button_ok.clicked.connect(self.button_ok)
    def radio_only_audio(self):
        self.file_format = '234'
    def radio_video(self):
        self.file_format = '22'
    def download_folder(self):
        os.makedirs('downloads', exist_ok=True)
        script_dir = os.path.dirname(sys.executable)
        download_dir = os.path.abspath(os.path.join(script_dir, 'downloads'))
        download_dir = f'''-o {download_dir}\\%(title)s.%(ext)s'''
        return download_dir

    def button_ok(self, checked=False):
        dirname = os.path.dirname(__file__)
        ayc = os.path.join(dirname, 'Resources/bin/yt-dlp.exe')
        url = self.ui.input_url.text()
        folder_dir = self.download_folder()
        if self.ui.button_only_audio.isChecked():
            self.radio_only_audio()
        elif self.ui.button_video.isChecked():
            self.radio_video()
        file_format_option = f"-f {self.file_format}"
        command = f'{ayc} {url} {file_format_option} {folder_dir}'
        print(f"Command: {command}")
        print(f"Working Directory: {os.getcwd()}")

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            exit_code = process.returncode

            if exit_code == 0:
                self.w = DoneWindow()
                self.w.show()
            else:
                print(f"The command failed with exit code: {exit_code}")
                print(f"Error message: {err.decode('utf-8')}")

        except Exception as e:
            print(f"Exception: {e}")

        
    def button_cancel(self, checked=False):
        sys.exit()
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    print(f"Executable Path: {sys.executable}")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()