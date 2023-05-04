# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled_main_test0429.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStatusBar, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QSize(1200, 800))
        MainWindow.setMaximumSize(QSize(1200, 800))
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionFixedSize = QAction(MainWindow)
        self.actionFixedSize.setObjectName(u"actionFixedSize")
        self.actionUnFixedSize = QAction(MainWindow)
        self.actionUnFixedSize.setObjectName(u"actionUnFixedSize")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.left_verticalLayout = QVBoxLayout()
        self.left_verticalLayout.setObjectName(u"left_verticalLayout")
        self.open_horizontalLayout = QHBoxLayout()
        self.open_horizontalLayout.setObjectName(u"open_horizontalLayout")
        self.open_file_button = QPushButton(self.centralwidget)
        self.open_file_button.setObjectName(u"open_file_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_file_button.sizePolicy().hasHeightForWidth())
        self.open_file_button.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(16)
        self.open_file_button.setFont(font)

        self.open_horizontalLayout.addWidget(self.open_file_button)

        self.open_with_default_button = QPushButton(self.centralwidget)
        self.open_with_default_button.setObjectName(u"open_with_default_button")
        sizePolicy.setHeightForWidth(self.open_with_default_button.sizePolicy().hasHeightForWidth())
        self.open_with_default_button.setSizePolicy(sizePolicy)
        self.open_with_default_button.setFont(font)

        self.open_horizontalLayout.addWidget(self.open_with_default_button)


        self.left_verticalLayout.addLayout(self.open_horizontalLayout)

        self.filename_text_browser = QTextBrowser(self.centralwidget)
        self.filename_text_browser.setObjectName(u"filename_text_browser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.filename_text_browser.sizePolicy().hasHeightForWidth())
        self.filename_text_browser.setSizePolicy(sizePolicy1)
        self.filename_text_browser.setFont(font)

        self.left_verticalLayout.addWidget(self.filename_text_browser)

        self.main_image_label = QLabel(self.centralwidget)
        self.main_image_label.setObjectName(u"main_image_label")
        self.main_image_label.setSizeIncrement(QSize(0, 0))
        self.main_image_label.setBaseSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(22)
        self.main_image_label.setFont(font1)
        self.main_image_label.setAcceptDrops(True)
        self.main_image_label.setAlignment(Qt.AlignCenter)

        self.left_verticalLayout.addWidget(self.main_image_label)

        self.gallery_display_layout = QHBoxLayout()
        self.gallery_display_layout.setObjectName(u"gallery_display_layout")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setEnabled(True)
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 653, 150))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gallery_display_layout.addWidget(self.scrollArea)

        self.gallery_refresh_button = QPushButton(self.centralwidget)
        self.gallery_refresh_button.setObjectName(u"gallery_refresh_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gallery_refresh_button.sizePolicy().hasHeightForWidth())
        self.gallery_refresh_button.setSizePolicy(sizePolicy2)
        self.gallery_refresh_button.setMinimumSize(QSize(60, 60))
        self.gallery_refresh_button.setMaximumSize(QSize(60, 60))
        self.gallery_refresh_button.setStyleSheet(u"background-color: transparent; border: none;")

        self.gallery_display_layout.addWidget(self.gallery_refresh_button)

        self.gallery_display_layout.setStretch(0, 7)
        self.gallery_display_layout.setStretch(1, 1)

        self.left_verticalLayout.addLayout(self.gallery_display_layout)

        self.left_verticalLayout.setStretch(0, 1)
        self.left_verticalLayout.setStretch(1, 1)
        self.left_verticalLayout.setStretch(2, 12)
        self.left_verticalLayout.setStretch(3, 4)

        self.horizontalLayout_2.addLayout(self.left_verticalLayout)

        self.right_verticalLayout = QVBoxLayout()
        self.right_verticalLayout.setObjectName(u"right_verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.postive_label = QLabel(self.groupBox)
        self.postive_label.setObjectName(u"postive_label")
        self.postive_label.setFont(font)
        self.postive_label.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.postive_label)

        self.positive_text_browser = QTextBrowser(self.groupBox)
        self.positive_text_browser.setObjectName(u"positive_text_browser")
        self.positive_text_browser.setFont(font)

        self.verticalLayout_2.addWidget(self.positive_text_browser)

        self.negative_label = QLabel(self.groupBox)
        self.negative_label.setObjectName(u"negative_label")
        self.negative_label.setFont(font)

        self.verticalLayout_2.addWidget(self.negative_label)

        self.negative_text_browser = QTextBrowser(self.groupBox)
        self.negative_text_browser.setObjectName(u"negative_text_browser")
        self.negative_text_browser.setFont(font)

        self.verticalLayout_2.addWidget(self.negative_text_browser)

        self.settings_label = QLabel(self.groupBox)
        self.settings_label.setObjectName(u"settings_label")
        self.settings_label.setFont(font)

        self.verticalLayout_2.addWidget(self.settings_label)

        self.settings_text_browser = QTextBrowser(self.groupBox)
        self.settings_text_browser.setObjectName(u"settings_text_browser")
        self.settings_text_browser.setFont(font)

        self.verticalLayout_2.addWidget(self.settings_text_browser)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 8)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 8)
        self.verticalLayout_2.setStretch(4, 1)
        self.verticalLayout_2.setStretch(5, 6)

        self.right_verticalLayout.addWidget(self.groupBox)

        self.copy_horizontalLayout = QHBoxLayout()
        self.copy_horizontalLayout.setObjectName(u"copy_horizontalLayout")
        self.copy_combo_box = QComboBox(self.centralwidget)
        self.copy_combo_box.addItem("")
        self.copy_combo_box.addItem("")
        self.copy_combo_box.setObjectName(u"copy_combo_box")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.copy_combo_box.sizePolicy().hasHeightForWidth())
        self.copy_combo_box.setSizePolicy(sizePolicy3)

        self.copy_horizontalLayout.addWidget(self.copy_combo_box)

        self.copy_button = QPushButton(self.centralwidget)
        self.copy_button.setObjectName(u"copy_button")
        sizePolicy.setHeightForWidth(self.copy_button.sizePolicy().hasHeightForWidth())
        self.copy_button.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(18)
        self.copy_button.setFont(font2)

        self.copy_horizontalLayout.addWidget(self.copy_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.copy_horizontalLayout.addItem(self.horizontalSpacer)

        self.edit_button = QPushButton(self.centralwidget)
        self.edit_button.setObjectName(u"edit_button")
        sizePolicy.setHeightForWidth(self.edit_button.sizePolicy().hasHeightForWidth())
        self.edit_button.setSizePolicy(sizePolicy)
        self.edit_button.setFont(font2)

        self.copy_horizontalLayout.addWidget(self.edit_button)

        self.copy_horizontalLayout.setStretch(0, 1)
        self.copy_horizontalLayout.setStretch(1, 1)
        self.copy_horizontalLayout.setStretch(2, 1)
        self.copy_horizontalLayout.setStretch(3, 1)

        self.right_verticalLayout.addLayout(self.copy_horizontalLayout)

        self.right_verticalLayout.setStretch(0, 12)
        self.right_verticalLayout.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.right_verticalLayout)

        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 24))
        self.menuOption = QMenu(self.menubar)
        self.menuOption.setObjectName(u"menuOption")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuOption.menuAction())
        self.menuOption.addAction(self.actionFixedSize)
        self.menuOption.addAction(self.actionUnFixedSize)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionFixedSize.setText(QCoreApplication.translate("MainWindow", u"FixedSize", None))
        self.actionUnFixedSize.setText(QCoreApplication.translate("MainWindow", u"UnFixedSize", None))
        self.open_file_button.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.open_with_default_button.setText(QCoreApplication.translate("MainWindow", u"Preview (Mac)", None))
        self.main_image_label.setText(QCoreApplication.translate("MainWindow", u"Drop to open", None))
        self.gallery_refresh_button.setText("")
        self.groupBox.setTitle("")
        self.postive_label.setText(QCoreApplication.translate("MainWindow", u"Positive", None))
        self.negative_label.setText(QCoreApplication.translate("MainWindow", u"Negative", None))
        self.settings_label.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.copy_combo_box.setItemText(0, QCoreApplication.translate("MainWindow", u"Copy_full", None))
        self.copy_combo_box.setItemText(1, QCoreApplication.translate("MainWindow", u"Copy_no_S", None))

        self.copy_button.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.edit_button.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuOption.setTitle(QCoreApplication.translate("MainWindow", u"Option", None))
    # retranslateUi

