import subprocess
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QGridLayout
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QGuiApplication, QKeyEvent
from PySide6.QtCore import Qt, Slot

from showmeprompt.ui_mainwindow_main_modify import Ui_MainWindow
from showmeprompt.get_image_exif import ImageInformation


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.ui.scrollAreaWidgetContents add QGridLayout layout
        self.scrollAreaWidgetContents_layout = QGridLayout()
        self.scrollAreaWidgetContents_layout.setObjectName(u"scrollAreaWidgetContents_layout")
        self.ui.scrollAreaWidgetContents.setLayout(self.scrollAreaWidgetContents_layout)

        # Set up main_image_label(QLabel) drag and drop events
        # self.ui.main_image_label.mousePressEvent = lambda event: self.open_and_show_image()
        self.ui.main_image_label.mousePressEvent = lambda event: self.show_image_use_preview(event)
        self.ui.main_image_label.dragEnterEvent = lambda event: self.main_image_label_dragEnterEvent(event)
        self.ui.main_image_label.dropEvent = lambda event: self.main_image_label_dropEvent(event)

        # Set up open, preview and refresh button and connect them with the corresponding functions
        self.ui.open_file_button.clicked.connect(self.open_and_show_image)
        self.ui.open_with_default_button.clicked.connect(self.show_image_use_preview)
        self.ui.gallery_refresh_button.clicked.connect(lambda: self.gallery(self.open_folder_path_last))
        # Disable the open_with_default_button (as there are no image files to open initially)
        self.ui.open_with_default_button.setEnabled(False)

        # Set up two copy buttons and connect them with the corresponding functions
        self.ui.copy_without_settings_button.clicked.connect(self.copy_raw_without_settings)
        self.ui.copy_raw_button.clicked.connect(self.copy_raw)

        self.open_folder_path_last = Path('.')
        self.file_path = Path('./fake_file_path')
        self.default_app = None
        self.current_image_raw_without_settings = ''
        self.current_image_raw = ''
        self._gallery_image_label_dict = {}
        self._gallery_images_file_path = []
        self._gallery_image_index_end = 0
        self._gallery_image_index_pointer = 0

    def keyPressEvent(self, event: QKeyEvent):
        """
        keyboard event(for A and S), A/S controls selecting different images.
        only works when self._gallery_image_label_dict is not empty
        :param event:
        :return:
        """
        if event.key() == Qt.Key_A and self._gallery_image_label_dict:
            if self._gallery_image_index_pointer > 0:
                file_path = self._gallery_images_file_path[self._gallery_image_index_pointer - 1]
                self.open_and_show_image(file_path)
        elif event.key() == Qt.Key_S and self._gallery_image_label_dict:
            if self._gallery_image_index_pointer < self._gallery_image_index_end:
                file_path = self._gallery_images_file_path[self._gallery_image_index_pointer + 1]
                self.open_and_show_image(file_path)

    def main_image_label_dragEnterEvent(self, event: QDragEnterEvent):
        """
        To handle drag events, and only accepts one image file at a time.
        :param event:
        :return:
        """
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            url = event.mimeData().urls()[0]
            if url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                event.acceptProposedAction()
        else:
            event.ignore()

    def main_image_label_dropEvent(self, event: QDropEvent) -> None:
        """
        To handle drop events, and get the file path of the image and calls self.open_and_show_image().
        :param event:
        :return:
        """
        url = event.mimeData().urls()[0]
        file_path = Path(url.toLocalFile())
        self.open_and_show_image(file_path)

    def open_and_show_image(self, file_path: Path = None) -> None:
        """
        Open the image and display, including updating the gallery and the index pointer
        :param file_path:
        :return:
        """
        # If opened through the open button, there will be no file_path
        if not file_path:
            selected_file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", str(self.open_folder_path_last),
                                                                "Image Files (*.png *.jpg *.jpeg *.webp)")
            if not _:
                return
            else:
                self.file_path = Path(selected_file_path)
        else:
            self.file_path = file_path

        file_folder_path = self.file_path.parent
        # Updating the gallery if the opened folder has been changed.
        if file_folder_path != self.open_folder_path_last:
            self.gallery(file_folder_path)
            # For opening files from the last accessed directory
            self.open_folder_path_last = file_folder_path

        # To read an image file and display it, including showing prompts
        pixmap = QPixmap(self.file_path)
        self.ui.main_image_label.setPixmap(pixmap.scaled(self.ui.main_image_label.size(),
                                                         Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation))
        self.show_info_to_text_browser(self.file_path)

        # After successfully opening an image for the first time, enable the preview button
        if not self.ui.open_with_default_button.isEnabled() and sys.platform == 'darwin':
            self.ui.open_with_default_button.setEnabled(True)

        # Updating self._gallery_image_index_pointer
        self._gallery_image_index_pointer = self._gallery_images_file_path.index(self.file_path)

    @Slot()
    def show_image_use_preview(self, event=None):
        """
        To open an image using the default program in Mac.
        """
        # todo: Currently, I don't have a Win system at hand to test.
        self.default_app = self.default_app or self.get_default_application()
        try:
            if not event:
                subprocess.call(self.default_app + [str(self.file_path)])
            elif event.button() == Qt.LeftButton and self.ui.main_image_label.pixmap():
                # for self.ui.main_image_label.mousePressEvent
                subprocess.call(self.default_app + [str(self.file_path)])
        except subprocess.CalledProcessError as e:
            print('Error:', e)

    def gallery(self, open_folder_path: Path = None) -> None:
        # print('\033[4m' + '\033[92m' + 'Refresh gallery ...' + '\033[0m')
        """
        This function is used to display the content of the gallery layout, including UI processing.
        :param open_folder_path:
        :return:None
        """
        if not open_folder_path:
            return

        # If there are widgets in the self.scrollAreaWidgetContents_layout(QGridLayout),
        # remove them first and clear self._gallery_image_label_dict.
        try:
            self.clear_layout_widgets(self.scrollAreaWidgetContents_layout)
            self._gallery_image_label_dict.clear()
        except Exception as e:
            print(e)

        self._gallery_images_file_path = sorted([file for file in open_folder_path.glob('*')
                                                 if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']])
        self._gallery_image_index_end = len(self._gallery_images_file_path) - 1  # index is 0~

        # Use a QLabel to display each image in the scrollAreaWidgetContents_layout,
        # with each image having its own label and bound to a click event.
        for i, image_path in enumerate(self._gallery_images_file_path):
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                continue
            label = QLabel()
            label.setPixmap(pixmap.scaledToHeight(95, Qt.SmoothTransformation))
            label.mousePressEvent = lambda event, path=image_path: self.open_and_show_image(path)
            self._gallery_image_label_dict[f'{image_path.name}'] = [label, image_path, i]
            self.scrollAreaWidgetContents_layout.addWidget(self._gallery_image_label_dict.get(f'{image_path.name}')[0],
                                                           0, i)

        # Update self._gallery_image_index_pointer for user clicked refresh button
        try:
            self._gallery_image_index_pointer = self._gallery_image_label_dict[f'{self.file_path.name}'][2]
        except KeyError as e:
            print(f'file {e} is deleted, move to first image')
            first_file_path = next(iter(self._gallery_image_label_dict.values()))[1]
            self.open_and_show_image(first_file_path)

    def copy_raw_without_settings(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.current_image_raw_without_settings)

    def copy_raw(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.current_image_raw)

    def show_info_to_text_browser(self, file_path: Path) -> None:
        """
        Reads the information of the image and displays the information in the corresponding text browser
        (filename, positive, negative, settings).
        The raw data is also saved for copying purposes.
        :param file_path:
        :return:
        """
        image_info = ImageInformation(self.file_path)
        self.ui.filename_text_browser.clear()
        self.ui.filename_text_browser.append(image_info.filename)
        self.ui.positive_text_browser.clear()
        self.ui.positive_text_browser.append(image_info.positive)
        self.ui.negative_text_browser.clear()
        self.ui.negative_text_browser.append(image_info.negative)
        self.ui.settings_text_browser.clear()
        self.ui.settings_text_browser.append(image_info.settings)
        self.current_image_raw_without_settings = image_info.raw_without_settings
        self.current_image_raw = image_info.raw

    @staticmethod
    def get_default_application() -> list | None:
        """
        Get the default application on the system (for Mac)
        :return:
        """
        try:
            all_app = subprocess.check_output(['mdfind', 'kMDItemContentTypeTree=com.apple.application-bundle']).decode(
                'utf-8')
            for line in all_app.splitlines():
                if 'Preview.app' in line:
                    path = line.strip()
                    return ['open', '-a', path]
        except subprocess.CalledProcessError as e:
            print('Error:', e)
        return None

    @staticmethod
    def clear_layout_widgets(layout) -> None:
        """
        Clear all widgets inside a layout.
        :param layout:
        :return:None
        """
        # while layout.count():
        #     widget = layout.takeAt(0).widget()
        #     if widget is not None:
        #         widget.deleteLater()
        #     else:
        #         self.clear_layout(item.layout())

        # As the content is known to consist of a single widget.
        # Optimization (no recursion needed).
        while layout.count():
            label = layout.takeAt(0).widget()
            if label is not None:
                label.deleteLater()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    # Set the main window to a fixed size so that the user cannot resize it.
    window.setFixedSize(1200, 760)
    window.show()
    sys.exit(app.exec())
