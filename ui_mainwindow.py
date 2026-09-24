# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QStatusBar, QWidget)
import qtresources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.btn_clic_connect = QPushButton(self.centralwidget)
        self.btn_clic_connect.setObjectName(u"btn_clic_connect")
        self.btn_clic_connect.setGeometry(QRect(50, 50, 281, 81))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(50, 140, 281, 28))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.line_edit_file = QLineEdit(self.layoutWidget)
        self.line_edit_file.setObjectName(u"line_edit_file")

        self.horizontalLayout.addWidget(self.line_edit_file)

        self.btn_browse = QPushButton(self.layoutWidget)
        self.btn_browse.setObjectName(u"btn_browse")

        self.horizontalLayout.addWidget(self.btn_browse)

        self.btn_home = QPushButton(self.centralwidget)
        self.btn_home.setObjectName(u"btn_home")
        self.btn_home.setGeometry(QRect(360, 50, 121, 41))
        self.btn_test = QPushButton(self.centralwidget)
        self.btn_test.setObjectName(u"btn_test")
        self.btn_test.setGeometry(QRect(370, 110, 141, 21))
        self.textconsole = QPlainTextEdit(self.centralwidget)
        self.textconsole.setObjectName(u"textconsole")
        self.textconsole.setGeometry(QRect(40, 250, 256, 231))
        self.btn_tcp_elements = QPushButton(self.centralwidget)
        self.btn_tcp_elements.setObjectName(u"btn_tcp_elements")
        self.btn_tcp_elements.setGeometry(QRect(40, 490, 251, 31))
        self.btn_quit = QPushButton(self.centralwidget)
        self.btn_quit.setObjectName(u"btn_quit")
        self.btn_quit.setGeometry(QRect(670, 10, 121, 41))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 220, 101, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(370, 240, 401, 141))
        self.label_2.setPixmap(QPixmap(u":/images/clic_very_good.svg"))
        self.label_2.setScaledContents(True)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(380, 390, 301, 141))
        self.btn_changevoltage = QPushButton(self.centralwidget)
        self.btn_changevoltage.setObjectName(u"btn_changevoltage")
        self.btn_changevoltage.setGeometry(QRect(360, 150, 121, 26))
        self.line_edit_targetVoltage = QLineEdit(self.centralwidget)
        self.line_edit_targetVoltage.setObjectName(u"line_edit_targetVoltage")
        self.line_edit_targetVoltage.setGeometry(QRect(490, 150, 51, 26))
        self.line_edit_rampRate = QLineEdit(self.centralwidget)
        self.line_edit_rampRate.setObjectName(u"line_edit_rampRate")
        self.line_edit_rampRate.setGeometry(QRect(560, 150, 51, 26))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menuCLiC_for_Nikon_Elements = QMenu(self.menubar)
        self.menuCLiC_for_Nikon_Elements.setObjectName(u"menuCLiC_for_Nikon_Elements")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuCLiC_for_Nikon_Elements.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_clic_connect.setText(QCoreApplication.translate("MainWindow", u"Connect to CLiC", None))
        self.line_edit_file.setText(QCoreApplication.translate("MainWindow", u"Config File...", None))
        self.btn_browse.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home CLiC to 0V", None))
        self.btn_test.setText(QCoreApplication.translate("MainWindow", u"Set to 100 V (TESTING)", None))
        self.btn_tcp_elements.setText(QCoreApplication.translate("MainWindow", u"Start Elements Communication", None))
        self.btn_quit.setText(QCoreApplication.translate("MainWindow", u"QUIT", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Console Log", None))
        self.label_2.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Author: Martin Jasinski<br/>Date: 9/24/2026</span></p><p><a href=\"https://github.com/leslielab/mj_clic4elements\"><span style=\" font-size:12pt; font-weight:700; text-decoration: underline; color:#003e92;\">Github</span></a><span style=\" font-size:12pt; font-weight:700;\"><br/><br/>LeslieLab, UBC, <br/>Licensed under GNU 3.0 or higher</span></p></body></html>", None))
        self.btn_changevoltage.setText(QCoreApplication.translate("MainWindow", u"changeVoltage", None))
        self.line_edit_targetVoltage.setText(QCoreApplication.translate("MainWindow", u"target", None))
        self.line_edit_rampRate.setText(QCoreApplication.translate("MainWindow", u"rate", None))
        self.menuCLiC_for_Nikon_Elements.setTitle(QCoreApplication.translate("MainWindow", u"CLiC for Nikon Elements", None))
    # retranslateUi

