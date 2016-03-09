# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we create a simple
window in PyQt4.

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
from PyQt4 import QtGui


def main():
    
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    w.resize(1000, 600)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    print("test")
    
    sys.exit(app.exec_())


def transferImgCV2QT(cv_img):
    #cv_img = cv2.imread('test.png')
    #cv_img =  cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)

    height, width, dim = cv_img.shape
    bytesPerLine = dim * width

    qt_img = QtGui.QImage(cv_img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)

    return qt_img

if __name__ == '__main__':
    main()