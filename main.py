import subprocess
import sys
from pathlib import Path

from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QLabel, QGridLayout,
                               QMessageBox, QStyle, QStyleFactory)
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QGuiApplication, QKeyEvent, QTextCharFormat, QFont
from PySide6.QtCore import Qt, Slot, QCoreApplication, QSize, QEvent

from showmeprompt.showmeprompt_main import Ui_MainWindow
from showmeprompt.get_image_exif import ImagePromptInfo
from showmeprompt.editor_window import EditRawWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.copy_button_size = self.ui.copy_button.size()

        self.setup_menu_action()
        self.setup_button_icon()
        self.setup_left_side_widget()
        self.setup_right_side_widget()

        # self.ui.scrollAreaWidgetContents add QGridLayout layout
        self.scrollAreaWidgetContents_layout = QGridLayout()
        self.scrollAreaWidgetContents_layout.setObjectName(u"scrollAreaWidgetContents_layout")
        self.ui.scrollAreaWidgetContents.setLayout(self.scrollAreaWidgetContents_layout)

        self.clipboard = QGuiApplication.clipboard()

        self.open_folder_path_last = Path('.')
        self.current_file_path = Path('./fake_file_path/fake_file.png')
        self.current_image_raw = ''
        self.current_image_raw_without_settings = ''
        self._prompt_cache = {}
        self._gallery_image_label_dict = {}
        self._gallery_image_file_path_list = []
        self._gallery_image_index_end = 0
        self._gallery_image_index_pointer = 0
        self._highlight_label_last = None
        self._gallery_image_label_axis_list = ()
        self._current_folder_is_empty = False

    def setup_menu_action(self) -> None:
        """
        Set connect for menu action: Option(FixedSize, UnFixedSize)
        """
        self.ui.actionFixedSize.triggered.connect(lambda: self.window_resizing())
        self.ui.actionUnFixedSize.triggered.connect(lambda: self.window_resizing(fixed=False))

    def setup_button_icon(self, use_builtin=True) -> None:
        """
        Set icon for open_file_button, open_with_default_button, gallery_refresh_button, edit_button
        (using built-in or using custom)
        """
        if use_builtin:
            self.ui.open_file_button.setIconSize(QSize(self.ui.open_file_button.size()))
            self.ui.open_file_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DirOpenIcon))
            self.ui.open_with_default_button.setIconSize(QSize(self.ui.open_with_default_button.size()))
            self.ui.open_with_default_button.setIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogListView))
            self.ui.gallery_refresh_button.setIconSize(QSize(self.ui.gallery_refresh_button.size()))
            self.ui.gallery_refresh_button.setIcon(QApplication.style().standardIcon(QStyle.SP_BrowserReload))
            self.ui.edit_button.setIconSize(self.ui.edit_button.size())
            self.ui.edit_button.setIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogContentsView))
        else:
            raise NotImplemented('No custom icons')

    def setup_left_side_widget(self) -> None:
        """
        Set event or connect for open_file_button, open_with_default_button(only for Mac), main_image_label,
        gallery_refresh_button
        """
        self.ui.open_file_button.clicked.connect(self.open_and_show_image)
        if sys.platform == 'darwin':
            self.get_default_application()
            self.ui.open_with_default_button.clicked.connect(self.show_image_use_preview)
            # self.ui.main_image_label.mousePressEvent = lambda event: self.open_and_show_image()
            self.ui.main_image_label.mousePressEvent = self.show_image_use_preview

        self.ui.main_image_label.dragEnterEvent = self.main_image_label_dragEnterEvent
        self.ui.main_image_label.dropEvent = self.main_image_label_dropEvent

        self.ui.gallery_refresh_button.clicked.connect(lambda: self.gallery(self.open_folder_path_last, True))

        # Disable open_with_default_button and gallery_refresh_button as there are no image files to open initially
        self.ui.open_with_default_button.setEnabled(False)
        self.ui.gallery_refresh_button.setEnabled(False)

    def setup_right_side_widget(self) -> None:
        """
        Set up copy and edit button, and connect them to their corresponding functions
        """
        self.setup_copy_full_button()  # default
        self.ui.copy_combo_box.currentTextChanged.connect(self.copy_combox_selected)

        self.ui.edit_button.clicked.connect(self.edit_prompt)
        # Disable the edit_button as there are no image files to open initially
        self.ui.edit_button.setEnabled(False)

    def window_resizing(self, fixed=True) -> None:
        """
        Set the Main Window size to be fixed at 1200x800, but allow for resizing with a minimum size of 950x760
        :param fixed: set True for fixed size
        """
        if fixed:
            self.setMinimumSize(1200, 800)
            self.setMaximumSize(1200, 800)
        else:
            self.setMinimumSize(950, 760)
            self.setMaximumSize(16777215, 16777215)

    def copy_combox_selected(self, combox_name: str) -> None:
        """
        Set the properties of the copy_button according to the content of the combobox
        :param combox_name: 'Copy_full' or 'Copy_no_S'
        """
        if combox_name == 'Copy_full':
            self.setup_copy_full_button()
        elif combox_name == 'Copy_no_S':
            self.setup_copy_without_settings_button()

    def setup_copy_full_button(self) -> None:
        """
        Set up the copy button for 'Copy-full'
        """
        self.ui.copy_button.setObjectName(u"copy_prompts_full_button")
        self.ui.copy_button.setIconSize(self.copy_button_size)
        self.ui.copy_button.setIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.ui.copy_button.clicked.connect(self.copy_prompts_full)

    def setup_copy_without_settings_button(self) -> None:
        """
        Set up the copy button for 'Copy-n-S'
        """
        self.ui.copy_button.setObjectName(u"copy_without_settings_button")
        self.ui.copy_button.setIconSize(self.copy_button_size)
        self.ui.copy_button.setIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.ui.copy_button.clicked.connect(self.copy_prompts_without_settings)

    def copy_prompts_full(self) -> None:
        """
        Copy full prompts and display the message on statusBar for 1.5 seconds
        """
        self.clipboard.setText(self.current_image_raw)
        self.ui.statusbar.setStyleSheet('color: green')
        self.ui.statusbar.showMessage('Copy full prompts', 1500)

    def copy_prompts_without_settings(self) -> None:
        """
        Copy prompts without settings and display the message on statusBar for 1.5 seconds
        """
        self.clipboard.setText(self.current_image_raw_without_settings)
        self.ui.statusbar.setStyleSheet('color: green')
        self.ui.statusbar.showMessage('Copy prompts without settings', 1500)

    def edit_prompt(self) -> None:
        """
        Pop up a QDialog window for modifying the prompts of the image
        """
        editor_window = EditRawWindow(file_path=self.current_file_path, image_raw=self.current_image_raw, parent=self)
        editor_window.rewrite_image_raw_signal.connect(lambda: self.update_image_prompt(self.current_file_path))
        editor_window.rewrite_image_raw_signal.connect(lambda: self.open_and_show_image(self.current_file_path))
        # Only after this QDialog is closed, the main window can be used again
        editor_window.setWindowModality(Qt.ApplicationModal)
        editor_window.show()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        keyboard event(for A and S), A/S controls selecting different images.
        only works when self._gallery_image_label_dict is not empty
        """
        if self._gallery_image_label_dict:
            if event.key() == Qt.Key_A:
                if self._gallery_image_index_pointer > 0:
                    file_path = self._gallery_image_file_path_list[self._gallery_image_index_pointer - 1]
                    self.open_and_show_image(file_path)
            elif event.key() == Qt.Key_S:
                if self._gallery_image_index_pointer < self._gallery_image_index_end:
                    file_path = self._gallery_image_file_path_list[self._gallery_image_index_pointer + 1]
                    self.open_and_show_image(file_path)

    def main_image_label_dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """
        To handle drag events, and only accepts one image file at a time.
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
        """
        url = event.mimeData().urls()[0]
        file_path = Path(url.toLocalFile())
        self.open_and_show_image(file_path)

    def open_and_show_image(self, file_path: Path = None, force=False) -> None:
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
        # Updating the gallery and self.open_folder_path_last if
        # 1. the opened folder has been changed
        # 2. force=True
        # 3. The situation where the images in the current folder are cleared and trigger corresponding processing,
        #    and then the images are put back to the folder.
        if file_folder_path != self.open_folder_path_last or force or self._current_folder_is_empty:
            self.gallery(file_folder_path)
            self.open_folder_path_last = file_folder_path
            self._current_folder_is_empty = False
            self._prompt_cache.clear()

        # To read an image file and display it, including showing prompt
        pixmap = QPixmap(self.current_file_path)
        if pixmap.isNull():
            return
        self.ui.main_image_label.setPixmap(pixmap.scaled(self.ui.main_image_label.size(),
                                                         Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation))
        self.show_prompt_to_text_browser()
        self.enable_buttons_when_open_image_success()

        # Updating self._gallery_image_index_pointer when the gallery does not need to refresh
        self._gallery_image_index_pointer = self._gallery_image_file_path_list.index(self.current_file_path)

        # Updating gallery highlight
        self.gallery_image_highlight(image_name=self.current_file_path.name)

    def show_prompt_to_text_browser(self) -> None:
        """
        Reads the information of the image and displays the information in the corresponding text browser
        (filename, positive, negative, settings).
        The raw data is also saved for copying purposes.
        """
        image_prompt = self.get_image_prompt(self.current_file_path)
        self.ui.filename_text_browser.clear()
        self.ui.filename_text_browser.append(image_prompt.filename)

        self.ui.positive_text_browser.clear()
        if image_prompt.positive:
            self.ui.positive_text_browser.append(image_prompt.positive)
        else:
            self.ui.positive_text_browser.insertHtml(
                "<span style='color: red;'>No Prompt information or parsing failed</span>")
            self.ui.positive_text_browser.setCurrentCharFormat(QTextCharFormat())

        self.ui.negative_text_browser.clear()
        self.ui.negative_text_browser.append(image_prompt.negative)

        self.ui.settings_text_browser.clear()
        self.ui.settings_text_browser.append(image_prompt.settings)

        self.current_image_raw_without_settings = image_prompt.raw_without_settings
        self.current_image_raw = image_prompt.raw

    def get_image_prompt(self, file_path: Path) -> ImagePromptInfo:
        """
        Get image's ImagePromptInfo instance
        """
        return self._prompt_cache.get(file_path) or self.update_image_prompt(file_path)

    def update_image_prompt(self, file_path: Path) -> ImagePromptInfo:
        """
        Updating image's ImagePromptInfo instance
        """
        image_prompt = ImagePromptInfo(file_path)
        self._prompt_cache[file_path] = image_prompt
        return image_prompt

    @Slot()
    def show_image_use_preview(self, event=None) -> None:
        """
        To open an image using the default program in Mac.
        :param event: accept mousePressEvent event
        """
        if not self.current_file_path.exists():
            self.handle_image_or_folder_deletion()
            return

        try:
            if not event or (event.button() == Qt.LeftButton and event.type() == QEvent.MouseButtonDblClick):
                subprocess.call(self.default_app_text_command + [str(self.current_file_path)])
        except subprocess.CalledProcessError as e:
            print('\033[33m' + f'Error: {e}, cannot call default application.' + '\033[0m')

    def get_default_application(self) -> None:
        """
        Get the default application 'Preview.app' command on the system (for Mac)
        """
        try:
            all_apps = subprocess.check_output(['mdfind', 'kMDItemContentTypeTree=com.apple.application-bundle']).decode('utf-8')
            for line in all_apps.splitlines():
                if 'Preview.app' in line:
                    path = line.strip()
                    self.default_app_text_command = ['open', '-a', path]
        except subprocess.CalledProcessError as e:
            print('\033[33m' + f'Error: {e}, cannot get default application.' + '\033[0m')

    def gallery(self, open_folder_path: Path, is_refresh=False) -> None:
        """
        To display the content of the gallery layout, including UI processing
        But in any case, it will try to clear the content of self.scrollAreaWidgetContents_layout
        :param open_folder_path: self.open_folder_path_last(if None)
        :param is_refresh: Set to True means called by clicking refresh button
        :return: None
        """
        # print('\033[4m' + '\033[92m' + 'Refresh gallery ...' + '\033[0m')
        if is_refresh:
            self._prompt_cache.clear()
        # If there are widgets in the self.scrollAreaWidgetContents_layout(QGridLayout),
        # remove them first and clear self._gallery_image_label_dict, self._gallery_image_file_path_list,
        # self._highlight_label_last(need to recycle the useless QLabel if exist)
        self.clear_layout_widgets(self.scrollAreaWidgetContents_layout)
        self._gallery_image_label_dict.clear()
        self._gallery_image_file_path_list.clear()
        if self._highlight_label_last:
            self._highlight_label_last = None

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
        # [Not using index with enumerate() because the file format may not be an image]
        index = 0
        for _, image_path in enumerate(images_file_path):
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                continue
            label = QLabel()
            label.setPixmap(pixmap.scaledToHeight(100, Qt.SmoothTransformation))
            label.mousePressEvent = lambda event, path=image_path: self.open_and_show_image(path)
            self._gallery_image_label_dict[f'{image_path.name}'] = [label, image_path, index]
            self.scrollAreaWidgetContents_layout.addWidget(label, 0, index)
            self._gallery_image_file_path_list.append(image_path)
            index += 1

        # Updating the self._gallery_image_index_end, self._gallery_image_index_pointer
        # and gallery_image_highlight
        self._gallery_image_index_end = len(self._gallery_image_file_path_list) - 1  # index is 0~
        self._gallery_image_index_pointer = self._gallery_image_file_path_list.index(self.current_file_path)
        self.gallery_image_highlight(image_name=self.current_file_path.name)

    @staticmethod
    def clear_layout_widgets(layout) -> None:
        """
        Clear all widgets inside a layout.
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

    def gallery_image_highlight(self, image_name: str) -> None:
        """
        Add a red border to the selected image and adjust the ScrollBar position accordingly
        :param image_name:
        :return:
        """
        self._gallery_image_label_axis_list = self.update_layout_and_get_coordinates()
        # Remove the last image's border
        if self._highlight_label_last:
            self._highlight_label_last.setStyleSheet(None)

        label = self._gallery_image_label_dict[image_name][0]
        label.setStyleSheet("border: 1px solid red;")
        self._highlight_label_last = label

        # When there are more than two images, keep at least the first two images
        index = max(self._gallery_image_index_pointer - 2, 0)
        axis_x = self._gallery_image_label_axis_list[index]
        self.ui.scrollArea.horizontalScrollBar().setValue(axis_x)

    def update_layout_and_get_coordinates(self) -> list:
        """
        Get the reference coordinates (x-axis) of all images currently in the gallery, and return a list
        :return:
        """
        QCoreApplication.processEvents()
        return [label[0].pos().x() for label in self._gallery_image_label_dict.values()]
        # print('\033[46m' + f'{self._gallery_image_label_axis_list= }' + '\033[0m')

    def enable_buttons_when_open_image_success(self) -> None:
        """
        Once an image is successfully opened, enable preview, refresh and edit buttons
        """
        self.ui.gallery_refresh_button.setEnabled(True)
        self.ui.edit_button.setEnabled(True)
        if sys.platform == 'darwin':
            self.ui.open_with_default_button.setEnabled(True)

    def handle_image_or_folder_deletion(self) -> None:
        """
        Handle the scenario where the user deletes the image currently being viewed or the folder it belongs to
        """
        if self.open_folder_path_last.exists():
            files_list = sorted([file for file in self.open_folder_path_last.glob('*')
                                 if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']])
            # If there is an image, open and show it
            for file in files_list:
                pixmap = QPixmap(file)
                if not pixmap.isNull():
                    self.open_and_show_image(file_path=file, force=True)
                    self.trigger_warning_dialog(situation='image_deletion')
                    return

            self.renew_ui()
            self._current_folder_is_empty = True  # for force to update gallery
            self.current_file_path = Path('./fake_file_path/file.png')
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
        """
        self.ui.gallery_refresh_button.setEnabled(False)
        self.ui.open_with_default_button.setEnabled(False)
        self.ui.edit_button.setEnabled(False)
        self.clear_layout_widgets(self.scrollAreaWidgetContents_layout)
        self.ui.main_image_label.clear()
        self.ui.main_image_label.setText("Drop to open")
        self.ui.filename_text_browser.clear()
        self.ui.positive_text_browser.clear()
        self.ui.negative_text_browser.clear()
        self.ui.settings_text_browser.clear()


if __name__ == "__main__":
    app = QApplication([])
    if sys.platform == 'darwin' and 'Fusion' in QStyleFactory.keys():
        app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
