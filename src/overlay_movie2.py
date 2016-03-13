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

def movie_overlay2():


    # 入力する動画と出力パスを指定。
    target = "target/test_input.mp4"
    result = "result/test_output.m4v"  #.m4vにしないとエラーが出る

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
    frameManager = frame_manager.FrameManager()
    
    
    while movie.isOpened():
        
        ret,frame = movie.read()

        if ret:
#        if ret and count > -1 and count < 200 :
            # グレースケールに変換
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 顔認識の実行
            facerecog = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
            
            # 認識した顔をFrameManagerに入れる
            managedFrame = frameManager.put(frame, facerecog)

            # 5回め以降はFrameManagerからフレームが返ってくるのでファイル出力
            if managedFrame is not None:

                # 認識した顔に画像を上乗せする
                for i in range(0,len(managedFrame.faces)):

                    # 扱いやすいように変数を用意
                    tmpCoord = managedFrame.faces[i].coordinate
                    tmpId = managedFrame.faces[i].id
                    
                    # 認識範囲にあわせて画像をリサイズ
                    resized_ol_image = resizeImage(ol_image, tmpCoord[2], tmpCoord[3])
                    
                    print("認識した顔の数(ID) = "+str(tmpId))
                    
                    # 特定のidのみ顔を上書き
                    if True:#tmpId < 20 :
                    
                        # オーバレイ画像の作成
                        managedFrame.frame = overlay(managedFrame.frame, resized_ol_image, [tmpCoord[0]+tmpCoord[2]/2,tmpCoord[1]+tmpCoord[3]/2])
                    
                        # 顔のIDを書き込み
                        cv2.putText(managedFrame.frame,str(tmpId),(tmpCoord[0],tmpCoord[1]),cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0))
    
                out.write(managedFrame.frame)
            if count%10 == 0:
                date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print(date + '現在フレーム数：'+str(count))
#        elif count > 200 :
        else:
            break
        
        count += 1

    print("出力フレーム数："+str(count))
    
# 画像のサイズを修正する
def resizeImage(image, height, width):
    
    # 元々のサイズを取得
    org_height, org_width = image.shape[:2]
    
    # 大きい方のサイズに合わせて縮小
    if float(height)/org_height > float(width)/org_width:
        ratio = float(height)/org_height
    else:
        ratio = float(width)/org_width
    
    resized = cv2.resize(image,(int(org_height*ratio),int(org_width*ratio)))
    
    return resized    

# PILを使って画像を合成
def overlayOnPart(src_image, overlay_image, posX, posY):

    # オーバレイ画像のサイズを取得
    ol_height, ol_width = overlay_image.shape[:2]

    # OpenCVの画像データをPILに変換
    #　BGRAからRGBAへ変換
    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    overlay_image_RGBA = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)
    
    #　PILに変換
    src_image_PIL=Image.fromarray(src_image_RGBA)
    overlay_image_PIL=Image.fromarray(overlay_image_RGBA)

    # 合成のため、RGBAモードに変更
    src_image_PIL = src_image_PIL.convert('RGBA')
    overlay_image_PIL = overlay_image_PIL.convert('RGBA')

    # 同じ大きさの透過キャンパスを用意
    tmp = Image.new('RGBA', src_image_PIL.size, (255, 255,255, 0))
    # 用意したキャンパスに上書き
    tmp.paste(overlay_image_PIL, (posX, posY), overlay_image_PIL)
    # オリジナルとキャンパスを合成して保存
    result = Image.alpha_composite(src_image_PIL, tmp)
    
    # COLOR_RGBA2BGRA から COLOR_RGBA2BGRに変更。アルファチャンネルを含んでいるとうまく動画に出力されない。
    return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)
        
if __name__ == '__main__':
    movie_overlay2()