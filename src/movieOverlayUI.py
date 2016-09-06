# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'movieOverlayUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 521, 361))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.framePosEdit = QtGui.QLineEdit(self.centralwidget)
        self.framePosEdit.setGeometry(QtCore.QRect(10, 380, 341, 20))
        self.framePosEdit.setObjectName(_fromUtf8("framePosEdit"))
        self.picNameEdit = QtGui.QLineEdit(self.centralwidget)
        self.picNameEdit.setGeometry(QtCore.QRect(10, 410, 341, 20))
        self.picNameEdit.setObjectName(_fromUtf8("picNameEdit"))
        self.zoomRateEdit = QtGui.QLineEdit(self.centralwidget)
        self.zoomRateEdit.setGeometry(QtCore.QRect(360, 410, 113, 20))
        self.zoomRateEdit.setObjectName(_fromUtf8("zoomRateEdit"))
        self.referButton = QtGui.QPushButton(self.centralwidget)
        self.referButton.setGeometry(QtCore.QRect(490, 410, 75, 23))
        self.referButton.setObjectName(_fromUtf8("referButton"))
        self.applyFrameEdit = QtGui.QLineEdit(self.centralwidget)
        self.applyFrameEdit.setGeometry(QtCore.QRect(360, 440, 113, 20))
        self.applyFrameEdit.setObjectName(_fromUtf8("applyFrameEdit"))
        self.applyButton = QtGui.QPushButton(self.centralwidget)
        self.applyButton.setGeometry(QtCore.QRect(490, 440, 75, 23))
        self.applyButton.setObjectName(_fromUtf8("applyButton"))
        self.prevButton = QtGui.QPushButton(self.centralwidget)
        self.prevButton.setGeometry(QtCore.QRect(10, 470, 75, 30))
        self.prevButton.setObjectName(_fromUtf8("prevButton"))
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(100, 470, 75, 30))
        self.nextButton.setObjectName(_fromUtf8("nextButton"))
        self.jumpFrameEdit = QtGui.QLineEdit(self.centralwidget)
        self.jumpFrameEdit.setGeometry(QtCore.QRect(210, 474, 113, 20))
        self.jumpFrameEdit.setObjectName(_fromUtf8("jumpFrameEdit"))
        self.jumpButton = QtGui.QPushButton(self.centralwidget)
        self.jumpButton.setGeometry(QtCore.QRect(330, 470, 75, 30))
        self.jumpButton.setObjectName(_fromUtf8("jumpButton"))
        self.outputButton = QtGui.QPushButton(self.centralwidget)
        self.outputButton.setGeometry(QtCore.QRect(400, 510, 75, 30))
        self.outputButton.setObjectName(_fromUtf8("outputButton"))
        self.exitButton = QtGui.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(490, 510, 75, 30))
        self.exitButton.setObjectName(_fromUtf8("exitButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.referButton.setText(_translate("MainWindow", "参照", None))
        self.applyButton.setText(_translate("MainWindow", "適用", None))
        self.prevButton.setText(_translate("MainWindow", "Prev", None))
        self.nextButton.setText(_translate("MainWindow", "Next", None))
        self.jumpButton.setText(_translate("MainWindow", "移動", None))
        self.outputButton.setText(_translate("MainWindow", "動画出力", None))
        self.exitButton.setText(_translate("MainWindow", "終了", None))

