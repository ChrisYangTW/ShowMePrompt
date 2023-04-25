import subprocess
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QGridLayout, QMessageBox
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
        # self.ui.main_image_label.mousePressEvent = lambda event: self.show_image_use_preview(event)
        self.ui.main_image_label.dragEnterEvent = lambda event: self.main_image_label_dragEnterEvent(event)
        self.ui.main_image_label.dropEvent = lambda event: self.main_image_label_dropEvent(event)

        # Set up open, preview and refresh button and connect them with the corresponding functions
        self.ui.open_file_button.clicked.connect(self.open_and_show_image)
        self.ui.open_with_default_button.clicked.connect(self.show_image_use_preview)
        self.ui.gallery_refresh_button.clicked.connect(lambda: self.gallery(self.open_folder_path_last))
        # Disable the open_with_default_button and gallery_refresh_button(as there are no image files to open initially)
        self.ui.open_with_default_button.setEnabled(False)
        self.ui.gallery_refresh_button.setEnabled(False)

        # Set up two copy buttons and connect them with the corresponding functions
        self.ui.copy_without_settings_button.clicked.connect(self.copy_raw_without_settings)
        self.ui.copy_raw_button.clicked.connect(self.copy_raw)

        self.open_folder_path_last = Path('.')
        self.current_file_path = Path('./fake_file_path/file.png')
        self.default_app = None
        self.current_image_raw_without_settings = ''
        self.current_image_raw = ''
        self._gallery_image_labels_dict = {}
        self._gallery_image_files_path_list = []
        self._gallery_image_index_end = 0
        self._gallery_image_index_pointer = 0

    def keyPressEvent(self, event: QKeyEvent):
        """
        keyboard event(for A and S), A/S controls selecting different images.
        only works when self._gallery_image_labels_dict is not empty
        :param event:
        :return:
        """
        if event.key() == Qt.Key_A and self._gallery_image_labels_dict:
            if self._gallery_image_index_pointer > 0:
                file_path = self._gallery_image_files_path_list[self._gallery_image_index_pointer - 1]
                self.open_and_show_image(file_path)
        elif event.key() == Qt.Key_S and self._gallery_image_labels_dict:
            if self._gallery_image_index_pointer < self._gallery_image_index_end:
                file_path = self._gallery_image_files_path_list[self._gallery_image_index_pointer + 1]
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

    def open_and_show_image(self, file_path: Path = None, force: bool = False) -> None:
        """
        Open the image and display, including updating the gallery and the index pointer
        :param file_path:
        :param force: set True to update gallery no matter what
        :return:
        """
        # If opened through the open button, there will be no file_path parameter
        if not file_path:
            selected_file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", str(self.open_folder_path_last),
                                                                "Image Files (*.png *.jpg *.jpeg *.webp)")
            if not _:
                return
            else:
                self.current_file_path = Path(selected_file_path)
        else:
            self.current_file_path = file_path
            if not self.current_file_path.exists():
                self.handle_image_or_folder_deletion()
                return

        file_folder_path = self.current_file_path.parent
        # Updating the gallery and self.open_folder_path_last if the opened folder has been changed or force=True
        if file_folder_path != self.open_folder_path_last or force:
            self.gallery(file_folder_path)
            self.open_folder_path_last = file_folder_path

        # To read an image file and display it, including showing prompts
        pixmap = QPixmap(self.current_file_path)
        if pixmap.isNull():
            return
        self.ui.main_image_label.setPixmap(pixmap.scaled(self.ui.main_image_label.size(),
                                                         Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation))
        self.show_info_to_text_browser(self.current_file_path)

        # Updating self._gallery_image_index_pointer when the gallery does not need to refresh
        self._gallery_image_index_pointer = self._gallery_image_files_path_list.index(self.current_file_path)

        # Once an image is successfully opened, enable the preview and refresh buttons if they were previously disabled
        if not self.ui.open_with_default_button.isEnabled() and sys.platform == 'darwin':
            self.ui.open_with_default_button.setEnabled(True)

        if not self.ui.gallery_refresh_button.isEnabled():
            self.ui.gallery_refresh_button.setEnabled(True)

    @Slot()
    def show_image_use_preview(self, event=None):
        """
        To open an image using the default program in Mac.
        """
        if not self.current_file_path.exists():
            self.handle_image_or_folder_deletion()
            return

        self.default_app = self.default_app or self.get_default_application()
        try:
            if not event:
                subprocess.call(self.default_app + [str(self.current_file_path)])
            elif event.button() == Qt.LeftButton and self.ui.main_image_label.pixmap():
                # for self.ui.main_image_label.mousePressEvent
                subprocess.call(self.default_app + [str(self.current_file_path)])
        except subprocess.CalledProcessError as e:
            print('Error:', e)

    def gallery(self, open_folder_path: Path = None) -> None:
        # print('\033[4m' + '\033[92m' + 'Refresh gallery ...' + '\033[0m')
        """
        To display the content of the gallery layout, including UI processing
        But in any case, it will try to clear the content of self.scrollAreaWidgetContents_layout
        :param open_folder_path: self.open_folder_path_last(if None)
        :return: None
        """
        if open_folder_path is None:
            open_folder_path = self.open_folder_path_last

        # If there are widgets in the self.scrollAreaWidgetContents_layout(QGridLayout),
        # remove them first and clear self._gallery_image_labels_dict & self._gallery_image_files_path_list
        self.clear_layout_widgets(self.scrollAreaWidgetContents_layout)
        self._gallery_image_labels_dict.clear()
        self._gallery_image_files_path_list.clear()

        # When the currently viewed image or its containing folder is deleted and the user clicks the refresh button
        # directly.
        # (Since deleting the folder is equivalent to deleting the image, it is sufficient to check if the image exists)
        if not self.current_file_path.exists():
            self.handle_image_or_folder_deletion()
            return

        images_file_path = sorted([file for file in open_folder_path.glob('*')
                                   if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']])

        # Use an QLabel to display an image in the scrollAreaWidgetContents_layout,
        # with each image having its own label and bound to a click event.
        for i, image_path in enumerate(images_file_path):
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                continue
            label = QLabel()
            label.setPixmap(pixmap.scaledToHeight(100, Qt.SmoothTransformation))
            label.mousePressEvent = lambda event, path=image_path: self.open_and_show_image(path)
            self._gallery_image_labels_dict[f'{image_path.name}'] = [label, image_path, i]
            self.scrollAreaWidgetContents_layout.addWidget(label, 0, i)
            self._gallery_image_files_path_list.append(image_path)

        # Updating the self._gallery_image_index_end and self._gallery_image_index_pointer
        self._gallery_image_index_end = len(self._gallery_image_files_path_list) - 1  # index is 0~
        self._gallery_image_index_pointer = self._gallery_image_files_path_list.index(self.current_file_path)

        # if self.current_file_path.exists():
        #     self._gallery_image_index_pointer = self._gallery_image_files_path_list.index(self.current_file_path)
        # else:
        #     print(f'{self.current_file_path} is deleted, move to first image.')
        #     first_file_path = next(iter(self._gallery_image_labels_dict.values()))[1]
        #     self.open_and_show_image(first_file_path)

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
        image_info = ImageInformation(file_path)
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
            all_apps = subprocess.check_output(['mdfind', 'kMDItemContentTypeTree=com.apple.application-bundle'])\
                .decode('utf-8')
            for line in all_apps.splitlines():
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

    def handle_image_or_folder_deletion(self) -> None:
        """
        Handle the scenario where the user deletes the image currently being viewed or the folder it belongs to
        :return:None
        """
        if self.open_folder_path_last.exists():
            files_list = sorted([file for file in self.open_folder_path_last.glob('*')
                                 if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']])
            for file in files_list:
                pixmap = QPixmap(file)
                if not pixmap.isNull():
                    print('do if statement')
                    self.open_and_show_image(file_path=file, force=True)
                    self.trigger_warning_dialog(situation='image_deletion')
                    return

            print('not do if statement')
            self.renew_ui()
            self.trigger_warning_dialog(situation='folder_empty')
        else:
            self.renew_ui()
            self.open_folder_path_last = Path('.')
            self.current_file_path = Path('./fake_file_path/file.png')
            self.trigger_warning_dialog(situation='folder_deletion')

    def trigger_warning_dialog(self, situation: str) -> None:
        """
        Display different QMessageBoxes based on different situations.
        situation: 'image_deletion' | 'folder_empty' | 'folder_deletion'
        :return:
        """
        match situation:
            case 'image_deletion':
                QMessageBox.warning(
                    self,
                    'Warning',
                    'The image is deleted\nWill display the first image in the folder',
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
            case 'folder_empty':
                QMessageBox.warning(
                    self,
                    'Warning',
                    'The folder has no image',
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
            case 'folder_deletion':
                QMessageBox.warning(
                    self,
                    'Warning',
                    'The folder is deleted',
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )

    def renew_ui(self) -> None:
        """
        Reset the UI to its initial state, but keep self.open_folder_path_last and self.current_file_path
        :return:
        """
        self.ui.gallery_refresh_button.setEnabled(False)
        self.ui.open_with_default_button.setEnabled(False)
        self.clear_layout_widgets(self.scrollAreaWidgetContents_layout)
        self.ui.main_image_label.clear()
        self.ui.main_image_label.setText("Drop to open")
        self.ui.filename_text_browser.clear()
        self.ui.positive_text_browser.clear()
        self.ui.negative_text_browser.clear()
        self.ui.settings_text_browser.clear()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    # Set the main window to a fixed size so that the user cannot resize it.
    window.setFixedSize(1200, 760)
    window.show()
    sys.exit(app.exec())
