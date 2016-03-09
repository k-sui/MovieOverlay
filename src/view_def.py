# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'closeapp.ui'
#
# Created: Tue Oct 21 10:59:12 2014
#      by: PyQt4 UI code generator 4.9.6
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
        MainWindow.resize(1500, 1000)
        self.graphic = QtGui.QGraphicsView(MainWindow)
        self.graphic.setGeometry(QtCore.QRect(0, 0, 720, 368))
        self.graphic.setObjectName(_fromUtf8("graphic"))

        self.textView = QtGui.QLineEdit(MainWindow)
        self.textView.move(20,660)
        self.textView.resize(300,20)

        
        self.olpicEdit = QtGui.QLineEdit(MainWindow)
        self.olpicEdit.move(20,690)
        self.olpicEdit.resize(300,20)

        self.zoomEdit = QtGui.QLineEdit(MainWindow)
        self.zoomEdit.move(320,690)
        self.zoomEdit.resize(40,20)

        self.chooseFileButton = QtGui.QPushButton(MainWindow)
        self.chooseFileButton.setGeometry(QtCore.QRect(370, 690, 40, 20))
        self.chooseFileButton.setObjectName(_fromUtf8("choose"))

        
        self.olpicApplyEdit = QtGui.QLineEdit(MainWindow)
        self.olpicApplyEdit.move(20,720)
        self.olpicApplyEdit.resize(200,20)

        self.olpicApplyButton = QtGui.QPushButton(MainWindow)
        self.olpicApplyButton.setGeometry(QtCore.QRect(120, 720, 100, 20))
        self.olpicApplyButton.setObjectName(_fromUtf8("jump"))


        self.nextButton = QtGui.QPushButton(MainWindow)
        self.nextButton.setGeometry(QtCore.QRect(180, 750, 320, 20))
        self.nextButton.setObjectName(_fromUtf8("Next"))

        self.prevButton = QtGui.QPushButton(MainWindow)
        self.prevButton.setGeometry(QtCore.QRect(20, 750, 160, 20))
        self.prevButton.setObjectName(_fromUtf8("Prev"))

        self.frameEdit = QtGui.QLineEdit(MainWindow)
        self.frameEdit.move(20,780)
        self.frameEdit.resize(100,20)

        self.jumpButton = QtGui.QPushButton(MainWindow)
        self.jumpButton.setGeometry(QtCore.QRect(120, 780, 200, 20))
        self.jumpButton.setObjectName(_fromUtf8("jump"))

        self.outputButton = QtGui.QPushButton(MainWindow)
        self.outputButton.setGeometry(QtCore.QRect(20, 810, 300, 30))
        self.outputButton.setObjectName(_fromUtf8("output"))

        self.exitButton = QtGui.QPushButton(MainWindow)
        self.exitButton.setGeometry(QtCore.QRect(20, 850, 300, 20))
        self.exitButton.setObjectName(_fromUtf8("exit"))

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.chooseFileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.chooseFile)
        QtCore.QObject.connect(self.olpicApplyButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.olpicApply)
        QtCore.QObject.connect(self.nextButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.next)
        QtCore.QObject.connect(self.prevButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.prev)
        QtCore.QObject.connect(self.jumpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.jump)
        QtCore.QObject.connect(self.exitButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.close)
        QtCore.QObject.connect(self.outputButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.output)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.chooseFileButton.setText(_translate("MainWindow", "参照", None))
        self.olpicApplyButton.setText(_translate("MainWindow", "適用", None))
        self.prevButton.setText(_translate("MainWindow", "Prev", None))
        self.nextButton.setText(_translate("MainWindow", "Next", None))
        self.jumpButton.setText(_translate("MainWindow", "Jump", None))
        self.outputButton.setText(_translate("MainWindow", "output", None))
        self.exitButton.setText(_translate("MainWindow", "exit", None))
