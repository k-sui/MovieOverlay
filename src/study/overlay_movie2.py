# -*- coding:utf-8 -*-

'''
Created on 2016/01/31

@author: master
'''

import cv2
import datetime
import numpy as np
from PIL import Image

import frame_manager

def overlay_movie2():

    # 入力する動画と出力パスを指定。
    target = "target/test_input.mp4"
    result = "result/test_output2.m4v"  #.m4vにしないとエラーが出る

    # 動画の読み込みと動画情報の取得
    movie = cv2.VideoCapture(target) 
    fps    = movie.get(cv2.CAP_PROP_FPS)
    height = movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width  = movie.get(cv2.CAP_PROP_FRAME_WIDTH)

    # 形式はMP4Vを指定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    
    # 出力先のファイルを開く
    out = cv2.VideoWriter(result, int(fourcc), fps, (int(width), int(height)))

    # カスケード分類器の特徴量を取得する
    cascade_path = "haarcascades/haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    # オーバーレイ画像の読み込み
    ol_imgae_path = "target/warai_otoko.png"    
    ol_image = cv2.imread(ol_imgae_path,cv2.IMREAD_UNCHANGED)
    
    # FrameManagerの作成
    frameManager = frame_manager.FrameManager(height, width)

    #　認識した顔を囲む矩形の色を指定。ここでは白。
    color = (255, 255, 255) 
    
    # 最初の1フレームを読み込む
    if movie.isOpened() == True:
        ret,frame = movie.read()
    else:
        ret = False

    count = 0

    # フレームの読み込みに成功している間フレームを書き出し続ける
    while ret:
        
        # グレースケールに変換
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔認識の実行
        facerecog = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
            
        # 認識した顔をFrameManagerに入れる
        managedFrame = frameManager.put(frame, facerecog)

        # 5回め以降はFrameManagerからフレームが返ってくるのでファイル出力
        if managedFrame is not None:

            # 認識した顔に番号を書き加える
            for i in range(0,len(managedFrame.faces)):

                # 扱いやすいように変数を用意
                tmpCoord = managedFrame.faces[i].coordinate
                tmpId = managedFrame.faces[i].id
                    
                print("認識した顔の数(ID) = "+str(tmpId))
                                        
                # 矩形で囲む
                cv2.rectangle(managedFrame.frame, tuple(tmpCoord[0:2]),tuple(tmpCoord[0:2]+tmpCoord[2:4]), color, thickness=2)
                    
                # 顔のIDを書き込み
                cv2.putText(managedFrame.frame,str(tmpId),(tmpCoord[0],tmpCoord[1]),cv2.FONT_HERSHEY_TRIPLEX, 2, (100,200,255), thickness=2)
    
            out.write(managedFrame.frame)
        if count%10 == 0:
            date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            print(date + '現在フレーム数：'+str(count))
        
        count += 1
        ret,frame = movie.read()

        # 途中終了
        if count > 200 :
            break

    print("出力フレーム数："+str(count))

    
if __name__ == '__main__':
    overlay_movie2()