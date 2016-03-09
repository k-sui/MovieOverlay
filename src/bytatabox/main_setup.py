# -*- coding: cp932 -*-
from __future__ import with_statement

import numpy as np
import sys
from PyQt4 import QtCore,QtGui
import os
from pyqt_Opencv import Ui_Qt_CV_MainWindow
#opencv_test�t�@�C���̓ǂݍ���
from opencv_test import opencv_test

class DesignerMainWindow(QtGui.QMainWindow,Ui_Qt_CV_MainWindow):
    def __init__(self, parent = None):
        super(DesignerMainWindow, self).__init__(parent)
        self.ui = Ui_Qt_CV_MainWindow()
        self.setupUi(self)
        QtCore.QObject.connect(self.file_button,QtCore.SIGNAL("clic��ked()"),self.open_file)
        #execute�{�^���N���b�N����exe_canny�֐������s
        QtCore.QObject.connect(self.exec_button,QtCore.SIGNAL("clicked()"),self.exe_canny)
    def open_file(self):
        self.file = QtGui.QFileDialog.getOpenFileName()
        if file:
            self.file_edit.setText(self.file[0])
            self.scene = QtGui.QGraphicsScene()
            pic_Item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.file[0]))
            __width = pic_Item.boundingRect().width()
            __height = pic_Item.boundingRect().height()
            __x = self.pic_View.x()
            __y = self.pic_View.y()
            self.pic_View.setGeometry(QtCore.QRect(__x, __y, __width, __height))

            __main_x = int(__x + __width + 20)
            __main_y = int(__y + __height + 50)
            self.resize(__main_x,__main_y)
            self.scene.addItem(pic_Item)
            self.pic_View.setScene(self.scene)
        return file
 #exe_canny�֐��Fopecv��canny�����摜��Qt��QPixmap�ɕϊ����`��

def exe_canny(self):
 	    #opencv_test�t�@�C������N���X�̓ǂݍ���
	    cv_test = opencv_test()
	    #�t�@�C����ǂݍ����R��B������
	    pic,pic2 = cv_test.open_pic(self.file[0])
	    #�G�b�W���o
	    self.cv_img = cv_test.canny(pic2)
	    #�摜�̍����A����ǂݍ���
	    height, width, dim = self.cv_img.shape
	    #�S�s�N�Z����
	    bytesPerLine = dim * width
	    #Opencv�inumpy�j�摜��Qt��QImage�ɕϊ�
	    self.image = QtGui.QImage(self.cv_img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
	    #QImage��QPixmap�ɕϊ����A�A�C�e���Ƃ��ēǂݍ���
	    pic_Item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.image))
	    #�摜��`��
	    self.scene.addItem(pic_Item)
 
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	dmw = DesignerMainWindow()
	dmw.show()
	sys.exit(app.exec_())