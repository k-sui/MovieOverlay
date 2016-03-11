# -*- coding: utf-8 -*-

import sys,os
from PyQt4 import QtCore,QtGui
import cv2
from view_def import *


import datetime
import numpy as np
from PIL import Image


class MyForm(QtGui.QMainWindow):

    repeatTime = 100 # ms

    nowFrame = 0
    REDUCT_RATE = 5

    RADIUS = 10

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #camera setup
        target = "L:\cvtest/target/starwars.mp4"
        self.movie = cv2.VideoCapture(target)  

        # 総フレーム数/REDUCT_RATEの配列を確保。初期化。
        faceNum = int(self.movie.get(cv2.CAP_PROP_FRAME_COUNT)/self.REDUCT_RATE + 1)
        self.faces = [[-1, -1, "", 100.0] for j in range(faceNum)]

        if self.movie.isOpened() is False:
            raise("IO Error")

        #window setup
        self.scene = QtGui.QGraphicsScene()
        self.set()

        
    def set(self):

        # 画像領域をクリア
        self.scene.clear()

        # 現在のフレームの位置をセットする
        self.movie.set(cv2.CAP_PROP_POS_FRAMES,self.nowFrame)
        ret, movieFrame = self.movie.read()
        if ret == False:
            return
        # オーバレイ画像が選択されており、読み込み成功していればオーバレイ
        ol_imgae_path = self.faces[int(self.nowFrame/self.REDUCT_RATE)][2]
        ol_image = cv2.imread(ol_imgae_path,cv2.IMREAD_UNCHANGED)
        if ol_image is not None and self.faces[int(self.nowFrame/self.REDUCT_RATE)][0]>-1:
            movieFrame = self.overlay(movieFrame, ol_image, self.faces[int(self.nowFrame/self.REDUCT_RATE)][0], self.faces[int(self.nowFrame/self.REDUCT_RATE)][1], self.faces[int(self.nowFrame/self.REDUCT_RATE)][3])

        movieFrame = cv2.cvtColor(movieFrame,cv2.COLOR_BGR2RGB)
        height, width, dim = movieFrame.shape
        bytesPerLine = dim * width
        self.image = QtGui.QImage(movieFrame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.image))
        #self.item.setPos(0,0)
        self.scene.addItem(self.item)

        # 顔の位置を選択してあれば赤丸を表示 端には丸を表示しない
        if self.faces[int(self.nowFrame/self.REDUCT_RATE)][0] > self.RADIUS/2 and self.faces[int(self.nowFrame/self.REDUCT_RATE)][1] > self.RADIUS/2:
            circleItem = QtGui.QGraphicsEllipseItem(self.faces[int(self.nowFrame/self.REDUCT_RATE)][0]-self.RADIUS/2, self.faces[int(self.nowFrame/self.REDUCT_RATE)][1]-self.RADIUS/2, self.RADIUS, self.RADIUS)
            circleItem.setPen(QtGui.QPen(QtCore.Qt.black, 1))
            circleItem.setBrush(QtGui.QBrush(QtCore.Qt.red))
            self.scene.addItem(circleItem)
        
        self.ui.graphic.installEventFilter(self)
        self.ui.graphic.setScene(self.scene)

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
        self.ui.textView.setText(viewtxt)
        
        self.ui.olpicEdit.setText(self.faces[int(self.nowFrame/self.REDUCT_RATE)][2])

        self.ui.zoomEdit.setText(str(self.faces[int(self.nowFrame/self.REDUCT_RATE)][3]))

    # 画像表示用のビューに対するイベントを定義
    def eventFilter(self, source, event):
        #マウスクリック時
        if (event.type() == QtCore.QEvent.MouseButtonPress and source is self.ui.graphic):
            #右クリックなら消去
            if event.button() == QtCore.Qt.RightButton:
                self.setFace(-1,-1)
            else:
                # カーソルの位置を取得
                pos = event.pos()

                # 顔の位置として保存
                self.setFace(pos.x(), pos.y())

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


    def jump(self):
        # 数値でない場合は無視
        if self.ui.frameEdit.text().isdigit():
            frameNum = int(self.ui.frameEdit.text())
            #フレーム数よりも大きい場合は無視
            if frameNum < self.movie.get(cv2.CAP_PROP_FRAME_COUNT):
                frameNum = frameNum - frameNum % self.REDUCT_RATE
                self.nowFrame = frameNum
                self.set()

    def olpicApply(self):
        picName = self.ui.olpicEdit.text()
        

        # 拡大率を取得。拡大率が正の数でない場合は100%として扱う
        if self.ui.zoomEdit.text().replace(".","",1).isdigit() == False or float(self.ui.zoomEdit.text()) < 0:
            zoom = 100.0
        else:
            zoom = float(self.ui.zoomEdit.text())


        # 数値でない場合は現在のフレームにだけ保存
        if self.ui.olpicApplyEdit.text().replace(".","",1).isdigit():
            applyTo = int(self.ui.olpicApplyEdit.text())
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


    def chooseFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName()
        self.ui.olpicEdit.setText(fileName)
        self.faces[int(self.nowFrame/self.REDUCT_RATE)][2]=fileName

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
                    allFaces[i*self.REDUCT_RATE+j][0] = (self.faces[i+1][0]-self.faces[i][0])/self.REDUCT_RATE + self.faces[i][0]
                    allFaces[i*self.REDUCT_RATE+j][1] = (self.faces[i+1][1]-self.faces[i][1])/self.REDUCT_RATE + self.faces[i][1]
                    allFaces[i*self.REDUCT_RATE+j][2] = self.faces[i][2]
                    allFaces[i*self.REDUCT_RATE+j][3] = (self.faces[i+1][3]-self.faces[i][3])/self.REDUCT_RATE + self.faces[i][3]

            # それ以外はそのフレームだけ書き出し
            else:
                allFaces[i*self.REDUCT_RATE] = self.faces[i]

        # 最後のフレームに顔があればそのまま書き出し
        if self.faces[reductedNum][0] != -1:
            allFaces[reductedNum*self.REDUCT_RATE] = self.faces[reductedNum]

        ################ここまでで顔位置データ作成#########################
        ###################ここから書き出し###############################
        # 書き込み先のファイルを開く
        result = "L:\cvtest/result/starwars.mp4" 
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(result, fourcc, 23.0, (720,368))
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
                frame = self.overlay(frame, self.ol_image, allFaces[i][0], allFaces[i][1], allFaces[i][3])
            if i== 1120:
                i = i

            out.write(frame)
            if i%50 == 0: 
                print("現在のフレーム："+str(i))
        
        out.release()


    # PILを使って画像を合成
    def overlay(self, src_image, overlay_image, posX, posY, zoom):

        # オーバレイ画像を倍率に合わせて拡大縮小
        resized_overlay_image = self.resize_image(overlay_image, zoom)

        # オーバレイ画像のサイズを取得
        ol_height, ol_width = resized_overlay_image.shape[:2]

        # OpenCVの画像データをPILに変換
    
        #　BGRAからRGBAへ変換
        src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
        resized_overlay_image_RGBA = cv2.cvtColor(resized_overlay_image, cv2.COLOR_BGRA2RGBA)
    
        #　PILに変換
        src_image_PIL=Image.fromarray(src_image_RGBA)
        resized_overlay_image_PIL=Image.fromarray(resized_overlay_image_RGBA)

        # 合成のため、RGBAモードに変更
        src_image_PIL = src_image_PIL.convert('RGBA')
        resized_overlay_image_PIL = resized_overlay_image_PIL.convert('RGBA')

        # 同じ大きさの透過キャンパスを用意
        tmp = Image.new('RGBA', src_image_PIL.size, (255, 255,255, 0))
        # rect[0]:x, rect[1]:y, rect[2]:width, rect[3]:height
        # 用意したキャンパスに上書き
        tmp.paste(resized_overlay_image_PIL, (int(posX-ol_height/2), int(posY-ol_width/2)), resized_overlay_image_PIL)
        # オリジナルとキャンパスを合成して保存
        result = Image.alpha_composite(src_image_PIL, tmp)

        return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)


    def resize_image(self, image, zoom):
    
        # 元々のサイズを取得
        org_height, org_width = image.shape[:2]

        ratio = float(zoom)/100
    
        # 大きい方のサイズに合わせて縮小
        resized = cv2.resize(image,(int(org_width*ratio),int(org_height*ratio)))
    
        return resized    

if __name__ == '__main__':
#    app = QtGui.QApplication(sys.argv)
#    viewer = Viewer()
#    viewer.show()
#    sys.exit(app.exec_())

    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
