# -*- coding: utf-8 -*-

import sys,os
from PyQt4 import QtCore,QtGui
import cv2
import common as common


import datetime
import numpy as np
from PIL import Image

import movieOverlayUI as ui

class MyForm(QtGui.QMainWindow):

    repeatTime = 100 # ms

    nowFrame = 0
    REDUCT_RATE = 1

    RADIUS = 10

    TARGET = "C:/Development/VSProject/MovieOverlay/target/アラジン.mp4"

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.importMovie(self.TARGET)

    # 動画の読み込み。targetにパスを指定
    def importMovie(self, target):

        self.movie = cv2.VideoCapture(target)  
        self.fps    = self.movie.get(cv2.CAP_PROP_FPS)
        self.height = self.movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width  = self.movie.get(cv2.CAP_PROP_FRAME_WIDTH)

        # 総フレーム数/REDUCT_RATEの配列を確保。初期化。
        faceNum = int(self.movie.get(cv2.CAP_PROP_FRAME_COUNT)/self.REDUCT_RATE + 1)
        self.faces = [[-1, -1, "", 100.0] for j in range(faceNum)]

        if self.movie.isOpened() is False:
            raise("IO Error")

        # GUI上の表示領域にセット
        self.scene = QtGui.QGraphicsScene()
        self.set()

        self.setSignals()

        
    def set(self):

        # 画像領域をクリア
        self.scene.clear()

        # 現在のフレームの位置をセットする
        self.movie.set(cv2.CAP_PROP_POS_FRAMES,self.nowFrame)
        ret, movieFrame = self.movie.read()
        if ret == False:
            return

        # オーバレイ画像が選択されていて、読み込み成功していればオーバレイ
        ol_imgae_path = self.faces[int(self.nowFrame/self.REDUCT_RATE)][2]
        ol_image = cv2.imread(ol_imgae_path,cv2.IMREAD_UNCHANGED)
        if ol_image is not None and self.faces[int(self.nowFrame/self.REDUCT_RATE)][0]>-1:
            movieFrame = common.overlayOnPart(movieFrame, ol_image, self.faces[int(self.nowFrame/self.REDUCT_RATE)][0], self.faces[int(self.nowFrame/self.REDUCT_RATE)][1], self.faces[int(self.nowFrame/self.REDUCT_RATE)][3])

        movieFrame = cv2.cvtColor(movieFrame,cv2.COLOR_BGR2RGB)
        height, width, dim = movieFrame.shape
        bytesPerLine = dim * width
        self.image = QtGui.QImage(movieFrame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.image))
        self.scene.addItem(self.item)

        # 顔の位置を選択してあれば赤丸を表示 端には丸を表示しない
        if self.faces[int(self.nowFrame/self.REDUCT_RATE)][0] > self.RADIUS/2 and self.faces[int(self.nowFrame/self.REDUCT_RATE)][1] > self.RADIUS/2:
            circleItem = QtGui.QGraphicsEllipseItem(self.faces[int(self.nowFrame/self.REDUCT_RATE)][0]-self.RADIUS/2, self.faces[int(self.nowFrame/self.REDUCT_RATE)][1]-self.RADIUS/2, self.RADIUS, self.RADIUS)
            circleItem.setPen(QtGui.QPen(QtCore.Qt.black, 1))
            circleItem.setBrush(QtGui.QBrush(QtCore.Qt.red))
            self.scene.addItem(circleItem)
        
        self.ui.graphicsView.installEventFilter(self)
        self.ui.graphicsView.setScene(self.scene)

        # 現在フレームを表示する文字列の作成、表示。
        viewtxt = ''
        viewtxt = viewtxt + '現在のフレーム： '
        viewtxt = viewtxt + str(self.nowFrame)
        viewtxt = viewtxt + ' / '
        viewtxt = viewtxt + str(self.movie.get(cv2.CAP_PROP_FRAME_COUNT))
        viewtxt = viewtxt + '   '
        viewtxt = viewtxt +str(self.faces[int(self.nowFrame/self.REDUCT_RATE)][0])
        viewtxt = viewtxt + ', '
        viewtxt = viewtxt +str(self.faces[int(self.nowFrame/self.REDUCT_RATE)][1])
        viewtxt = viewtxt + ')'
        self.ui.framePosEdit.setText(viewtxt)
        
        self.ui.picNameEdit.setText(self.faces[int(self.nowFrame/self.REDUCT_RATE)][2])
        self.ui.zoomRateEdit.setText(str(self.faces[int(self.nowFrame/self.REDUCT_RATE)][3]))

    # 画像表示用のビューに対するイベントを定義
    def eventFilter(self, source, event):
        #マウスクリック時
        if (event.type() == QtCore.QEvent.MouseButtonPress and source is self.ui.graphicsView):
            #右クリックなら消去
            if event.button() == QtCore.Qt.RightButton:
                self.setFace(-1,-1)
            else:
                # カーソルの位置を取得
                pos = event.pos()

                # 現在のQGraphicViewのスクロール位置を取得
                scrX = self.ui.graphicsView.horizontalScrollBar().value()
                scrY = self.ui.graphicsView.verticalScrollBar().value()

                # 顔の位置として保存
                self.setFace(pos.x()+scrX, pos.y()+scrY)

        # キーボード操作時
        elif (event.type() == QtCore.QEvent.KeyPress):
            # Aで戻る、Dで進む
            if event.key()==QtCore.Qt.Key_A:
                self.prev()
            elif event.key()==QtCore.Qt.Key_D:
                self.next()

        # 返さなきゃいけないらしい
        return QtGui.QWidget.eventFilter(self, source, event)

    def next(self):
        self.nowFrame +=self.REDUCT_RATE
        if self.nowFrame > self.movie.get(cv2.CAP_PROP_FRAME_COUNT):
            self.nowFrame -=self.REDUCT_RATE

        self.movie.set(cv2.CAP_PROP_POS_FRAMES,self.nowFrame)
        self.set()

        return True

    def prev(self):
        self.nowFrame -=self.REDUCT_RATE
        if self.nowFrame < 0 :
            self.nowFrame = 0

        self.movie.set(cv2.CAP_PROP_POS_FRAMES,self.nowFrame)

        self.set()

        return True

    def setFace(self, x, y):
        self.faces[int(self.nowFrame/self.REDUCT_RATE)][0] = x
        self.faces[int(self.nowFrame/self.REDUCT_RATE)][1] = y
        self.set()

    # 指定したフレームに移動する処理
    def jump(self):
        # 数値でない場合は無視
        if self.ui.jumpFrameEdit.text().isdigit():
            frameNum = int(self.ui.jumpFrameEdit.text())
            #フレーム数よりも大きい場合は無視
            if frameNum < self.movie.get(cv2.CAP_PROP_FRAME_COUNT):
                frameNum = frameNum - frameNum % self.REDUCT_RATE
                self.nowFrame = frameNum
                self.set()
    
    # オーバーレイする画像を変更する処理
    def olpicApply(self):
        picName = self.ui.picNameEdit.text()
        

        # 拡大率を取得。拡大率が正の数でない場合は100%として扱う
        if self.ui.zoomRateEdit.text().replace(".","",1).isdigit() == False or float(self.ui.zoomRateEdit.text()) < 0:
            zoom = 100.0
        else:
            zoom = float(self.ui.zoomRateEdit.text())


        # 数値でない場合は現在のフレームにだけ保存
        if self.ui.applyFrameEdit.text().replace(".","",1).isdigit():
            applyTo = int(self.ui.applyFrameEdit.text())
            #フレーム数よりも大きい場合は以降の全てに適用
            if applyTo > self.movie.get(cv2.CAP_PROP_FRAME_COUNT):
                applyTo = self.movie.get(cv2.CAP_PROP_FRAME_COUNT)
            applyTo = applyTo - applyTo % self.REDUCT_RATE

            #現在のフレームよりも前を指定した場合は現在のフレームにだけ保存
            if applyTo < self.nowFrame:
                self.faces[self.nowFrame/self.REDUCT_RATE][2] = picName
                self.faces[self.nowFrame/self.REDUCT_RATE][3] = float(zoom)

            # 現在のフレームから指定したフレームまで全てを同じ画像にする
            for i in range(int(self.nowFrame/self.REDUCT_RATE),int(applyTo/self.REDUCT_RATE)+1):
                self.faces[i][2] = picName
                self.faces[i][3] = float(zoom)

        else:
            self.faces[int(self.nowFrame/self.REDUCT_RATE)][2] = picName
            self.faces[int(self.nowFrame/self.REDUCT_RATE)][3] = float(zoom)

        self.set()

    # オーバーレイする画像を選択させる処理
    def chooseFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName()
        self.ui.picNameEdit.setText(fileName)
        self.faces[int(self.nowFrame/self.REDUCT_RATE)][2]=fileName

    # 動画を出力する処理
    def output(self):

        originNum = int(self.movie.get(cv2.CAP_PROP_FRAME_COUNT))
        reductedNum = int(self.movie.get(cv2.CAP_PROP_FRAME_COUNT)/self.REDUCT_RATE)

        # 減らしたフレームを補完しつつ、オーバーレイ位置の配列を作成
        allFaces = [[-1, -1, "",100.0] for j in range(originNum+1)]
        for i in range(reductedNum):
            if self.faces[i][0] == -1:
                dummy=1
            # 次のフレームに顔がなければそのフレームだけ書き出し
            elif self.faces[i+1][0] == -1:
                allFaces[i*self.REDUCT_RATE] = self.faces[i]            
            # オーバレイ画像が同じなら連続として処理
            elif self.faces[i][2] == self.faces[i+1][2]:
                for j in range(self.REDUCT_RATE):
                    allFaces[i*self.REDUCT_RATE+j][0] = (self.faces[i+1][0]-self.faces[i][0])/self.REDUCT_RATE * j + self.faces[i][0]
                    allFaces[i*self.REDUCT_RATE+j][1] = (self.faces[i+1][1]-self.faces[i][1])/self.REDUCT_RATE * j + self.faces[i][1]
                    allFaces[i*self.REDUCT_RATE+j][2] = self.faces[i][2]
                    allFaces[i*self.REDUCT_RATE+j][3] = (self.faces[i+1][3]-self.faces[i][3])/self.REDUCT_RATE * j + self.faces[i][3]

            # それ以外はそのフレームだけ書き出し
            else:
                allFaces[i*self.REDUCT_RATE] = self.faces[i]

        # 最後のフレームに顔があればそのまま書き出し
        if self.faces[reductedNum][0] != -1:
            allFaces[reductedNum*self.REDUCT_RATE] = self.faces[reductedNum]

        ################ここまでで顔位置データ作成#########################
        ###################ここから書き出し###############################
        # 書き込み先のファイルを開く
        result = "C:/Development/VSProject/MovieOverlay/result/arajin_v8.mp4" 
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(result, fourcc,  self.fps, (int(self.width), int(self.height)))
        self.ol_image_path=""
        self.ol_image=None

        self.movie.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for i in range(int(self.movie.get(cv2.CAP_PROP_FRAME_COUNT))):
            ret, frame = self.movie.read()
            if ret==False:
                break
            # オーバレイ画像が選択されており、読み込み成功していればオーバレイ
            if self.ol_image_path != allFaces[i][2]:
                self.ol_imgae_path = allFaces[i][2]
                self.ol_image = cv2.imread(self.ol_imgae_path,cv2.IMREAD_UNCHANGED)
            if self.ol_image is not None and allFaces[i][0]>-1:
                frame = common.overlayOnPart(frame, self.ol_image, allFaces[i][0], allFaces[i][1], allFaces[i][3])

            out.write(frame)
            if i%50 == 0: 
                print("現在のフレーム："+str(i))
        
        out.release()

    def setSignals(self):

        QtCore.QObject.connect(self.ui.referButton, QtCore.SIGNAL("clicked()"), self.chooseFile)
        QtCore.QObject.connect(self.ui.applyButton, QtCore.SIGNAL("clicked()"), self.olpicApply)
        QtCore.QObject.connect(self.ui.nextButton, QtCore.SIGNAL("clicked()"), self.next)
        QtCore.QObject.connect(self.ui.prevButton, QtCore.SIGNAL("clicked()"), self.prev)
        QtCore.QObject.connect(self.ui.jumpButton, QtCore.SIGNAL("clicked()"), self.jump)
        QtCore.QObject.connect(self.ui.exitButton, QtCore.SIGNAL("clicked()"), self.close)
        QtCore.QObject.connect(self.ui.outputButton, QtCore.SIGNAL("clicked()"), self.output)
        QtCore.QMetaObject.connectSlotsByName(self)

if __name__ == '__main__':


    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
