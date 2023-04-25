# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled_main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStatusBar, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1263, 760)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.open_file_button = QPushButton(self.centralwidget)
        self.open_file_button.setObjectName(u"open_file_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_file_button.sizePolicy().hasHeightForWidth())
        self.open_file_button.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.open_file_button)

        self.open_with_default_button = QPushButton(self.centralwidget)
        self.open_with_default_button.setObjectName(u"open_with_default_button")

        self.horizontalLayout.addWidget(self.open_with_default_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.filename_text_browser = QTextBrowser(self.centralwidget)
        self.filename_text_browser.setObjectName(u"filename_text_browser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.filename_text_browser.sizePolicy().hasHeightForWidth())
        self.filename_text_browser.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.filename_text_browser)

        self.main_image_label = QLabel(self.centralwidget)
        self.main_image_label.setObjectName(u"main_image_label")
        self.main_image_label.setAcceptDrops(True)
        self.main_image_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.main_image_label)

        self.gallery_display_layout = QHBoxLayout()
        self.gallery_display_layout.setObjectName(u"gallery_display_layout")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setEnabled(True)
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 650, 123))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gallery_display_layout.addWidget(self.scrollArea)

        self.gallery_refresh_button = QPushButton(self.centralwidget)
        self.gallery_refresh_button.setObjectName(u"gallery_refresh_button")

        self.gallery_display_layout.addWidget(self.gallery_refresh_button)

        self.gallery_display_layout.setStretch(0, 7)
        self.gallery_display_layout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.gallery_display_layout)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 12)
        self.verticalLayout.setStretch(3, 4)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.postive_label = QLabel(self.groupBox)
        self.postive_label.setObjectName(u"postive_label")

        self.verticalLayout_3.addWidget(self.postive_label)

        self.positive_text_browser = QTextBrowser(self.groupBox)
        self.positive_text_browser.setObjectName(u"positive_text_browser")

        self.verticalLayout_3.addWidget(self.positive_text_browser)

        self.negative_label = QLabel(self.groupBox)
        self.negative_label.setObjectName(u"negative_label")

        self.verticalLayout_3.addWidget(self.negative_label)

        self.negative_text_browser = QTextBrowser(self.groupBox)
        self.negative_text_browser.setObjectName(u"negative_text_browser")

        self.verticalLayout_3.addWidget(self.negative_text_browser)

        self.settings_label = QLabel(self.groupBox)
        self.settings_label.setObjectName(u"settings_label")

        self.verticalLayout_3.addWidget(self.settings_label)

        self.settings_text_browser = QTextBrowser(self.groupBox)
        self.settings_text_browser.setObjectName(u"settings_text_browser")

        self.verticalLayout_3.addWidget(self.settings_text_browser)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.copy_without_settings_button = QPushButton(self.groupBox)
        self.copy_without_settings_button.setObjectName(u"copy_without_settings_button")

        self.horizontalLayout_3.addWidget(self.copy_without_settings_button)

        self.copy_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.copy_horizontalSpacer)

        self.copy_raw_button = QPushButton(self.groupBox)
        self.copy_raw_button.setObjectName(u"copy_raw_button")

        self.horizontalLayout_3.addWidget(self.copy_raw_button)

        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 4)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 10)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 8)
        self.verticalLayout_3.setStretch(4, 1)
        self.verticalLayout_3.setStretch(5, 4)
        self.verticalLayout_3.setStretch(6, 1)

        self.horizontalLayout_2.addWidget(self.groupBox)

        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 3)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1263, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.open_file_button.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.open_with_default_button.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.main_image_label.setText(QCoreApplication.translate("MainWindow", u"Drop to open", None))
        self.gallery_refresh_button.setText("")
        self.groupBox.setTitle("")
        self.postive_label.setText(QCoreApplication.translate("MainWindow", u"Positive", None))
        self.negative_label.setText(QCoreApplication.translate("MainWindow", u"Negative", None))
        self.settings_label.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.copy_without_settings_button.setText(QCoreApplication.translate("MainWindow", u"without_S", None))
        self.copy_raw_button.setText(QCoreApplication.translate("MainWindow", u"full", None))
    # retranslateUi

