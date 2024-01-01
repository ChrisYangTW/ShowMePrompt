import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from showmeprompt.ShowMePromptMainWindow import MainWindow


if __name__ == "__main__":
    app = QApplication([])
    if sys.platform == 'darwin' and 'Fusion' in QStyleFactory.keys():
        app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
