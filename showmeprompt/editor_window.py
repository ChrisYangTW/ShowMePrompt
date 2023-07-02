from pathlib import Path

import piexif
import piexif.helper
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton, QMessageBox, QWidget


class EditRawWindow(QDialog):
    """
    QDialog window for editing image prompts
    """
    rewrite_image_raw_signal = Signal()

    def __init__(self, file_path: Path, image_raw='', parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Raw Window')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout(self)
        self.editor = QTextEdit(self)
        layout.addWidget(self.editor)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.setAutoDefault(False)
        self.cancel_button.setStyleSheet("background-color: rgb(255, 100, 50)")
        self.edit_button = QPushButton('Edit', self)
        self.edit_button.setStyleSheet("background-color: rgb(0, 195, 50)")
        self.edit_button.setAutoDefault(False)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.edit_button)

        layout.addLayout(button_layout)

        # Set up edit and cancel buttons, and connect them to their corresponding functions
        self.cancel_button.clicked.connect(self.reject)
        self.edit_button.clicked.connect(self.edit)

        # Move the QDialog window to the center of the main window
        if self.parentWidget():
            center_point = self.parentWidget().geometry().center()
            self.move(center_point.x() - self.width() / 2, center_point.y() - self.height() / 2)

        self.file_path = file_path
        self.image_raw = image_raw
        self.editor.setText(self.image_raw)

    def edit(self):
        """
        Pop up a QMessageBox to ask for confirmation to modify the prompts of the image.
        If 'Yes' is clicked, rewrite the prompts of the image, then send a signal to the main window to reload the
        image, and finally close the QDialog window.
        """
        text = self.editor.toPlainText()
        # When there are no modifications, close the window directly.
        if text == self.image_raw:
            self.done(0)
            return

        result = QMessageBox.question(self, 'Confirmation', 'Are you sure to edit this image?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            with Image.open(self.file_path) as img:
                if img.format == 'PNG':
                    metadata = PngInfo()
                    metadata.add_text('parameters', text)
                    img.save(self.file_path, pnginfo=metadata)
                else:  # Assuming main.py only supports *.png, *.jpg, *.jpeg, and *.webp files
                    exif_dict = piexif.load((img.info['exif']))
                    exif_dict['Exif'][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(text, 'unicode')
                    exif_bytes = piexif.dump(exif_dict)
                    img.save(self.file_path, exif=exif_bytes)

            self.rewrite_image_raw_signal.emit()
            self.done(0)

    # Overrides the reject() to allow users to cancel the dialog using the ESC key
    def reject(self):
        if  self.editor.toPlainText() == self.image_raw:
            self.done(0)
            return

        result = QMessageBox.question(self, 'Confirmation', 'Changes have been made. Exit without saving?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            self.done(0)


if __name__ == '__main__':
    from PySide6.QtWidgets import QMainWindow, QApplication
    from PySide6.QtGui import Qt

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.setWindowTitle('Button Window')
            self.setGeometry(100, 100, 800, 600)
            widget = QWidget()
            v_layout = QVBoxLayout()
            widget.setLayout(v_layout)
            self.setCentralWidget(widget)

            self.button = QPushButton('Open Editable Window', self)
            self.button.clicked.connect(self.show_editable_window)
            v_layout.addWidget(self.button)

        def show_editable_window(self):
            editable_window = EditRawWindow(file_path=Path(), parent=self)
            editable_window.setWindowModality(Qt.ApplicationModal)
            editable_window.show()


    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
