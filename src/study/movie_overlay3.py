#coding=utf-8

'''
Created on 2016/01/31

@author: master
'''

import cv2
import datetime
import numpy as np
from PIL import Image

import frame_manager
import queue

def movie_overlay3():

#    target = "../target/smile.mp4"
    target = "L:\cvtest/target/ameniutaeba.mp4"
    result = "L:\cvtest/result/ameniutaeba.mp4" 
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # 顔認識用特徴量のファイル指定
    cascade_path = "L:\Anaconda3/Library/etc/haarcascades/haarcascade_frontalface_alt.xml"
#    cascade_path = "L:\Anaconda3/Library/etc/haarcascades/haarcascade_profileface.xml"
#    cascade_path = "L:\Anaconda3/Library/etc/lbpcascades/lbpcascade_profileface.xml"
    #　認識した顔の色を指定。ここでは白。
    color = (255, 255, 255) 
    
    # FrameManagerの作成
    frameManager = frame_manager.FrameManager()
    
    # 顔情報保管用のキューの作成
    faceQueue = queue.Queue()

    movie = cv2.VideoCapture(target)    
    out = cv2.VideoWriter(result, fourcc, 23.0, (720,276))
    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)

    # オーバーレイ画像の読み込み
    ol_imgae_path = "L:\cvtest/target/warai_otoko.png"    
    ol_image = cv2.imread(ol_imgae_path,cv2.IMREAD_UNCHANGED)
    
    
    count = 0
    
    while movie.isOpened():
        
        ret,frame = movie.read()

#        if ret:
        if ret and count > -1 and count < 200 :
            # グレースケールに変換
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 顔認識の実行
            facerecog = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
            
            # 認識した顔をFrameManagerに入れる
            managedFrame = frameManager.put(frame, facerecog)

            # 5回め以降はFrameManagerからフレームが返ってくるのでファイル出力
            if managedFrame is not None:

                # 認識した顔に画像を上乗せする
#                for i in range(0,len(managedFrame.faces)):

                    # 扱いやすいように変数を用意
#                    tmpCoord = managedFrame.faces[i].coordinate
#                    tmpId = managedFrame.faces[i].id
                    
                    # 認識範囲にあわせて画像をリサイズ
#                    resized_ol_image = resize_image(ol_image, tmpCoord[2], tmpCoord[3])
                    
#                    print("認識した顔の数(ID) = "+str(tmpId))
                    
                    # 特定のidのみ顔を上書き
#                    if True:#tmpId < 20 :
                    
                        # オーバレイ画像の作成
#                        managedFrame.frame = overlay(managedFrame.frame, resized_ol_image, [tmpCoord[0]+tmpCoord[2]/2,tmpCoord[1]+tmpCoord[3]/2])
                    
                        # 顔のIDを書き込み
#                        cv2.putText(managedFrame.frame,str(tmpId),(tmpCoord[0],tmpCoord[1]),cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0))
                # 認識した顔に画像を上乗せする
                managedFrame.frame = overlay_faces(managedFrame.frame, ol_image, managedFrame.faces, True)
    
                out.write(managedFrame.frame)
                
                # フレームごとの顔情報をキューに保存
                faceQueue.put(managedFrame.faces)
                
            if count%10 == 0:
                date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print(date + '現在フレーム数：'+str(count))
        elif count > 200 :
#        else:
            break
        
        count += 1

    # FrameManagerにまだフレームが残っているので全て読み出す
    managedFrame = frameManager.put(None, None)
    while managedFrame is not None:
        # 認識した顔に画像を上乗せする
        managedFrame.frame = overlay_faces(managedFrame.frame, ol_image, managedFrame.faces, True)

        out.write(managedFrame.frame)
        
        # フレームごとの顔情報をキューに保存
        faceQueue.put(managedFrame.faces)

        # 次のフレームの読みだし
        managedFrame = frameManager.put(None, None)

        
    print("出力フレーム数："+str(count))
    

def resize_image(image, height, width):
    
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
def overlay(src_image, overlay_image, coordinate):

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
    # rect[0]:x, rect[1]:y, rect[2]:width, rect[3]:height
    # 用意したキャンパスに上書き
    tmp.paste(overlay_image_PIL, (int(coordinate[0]-ol_height/2), int(coordinate[1]-ol_width/2)), overlay_image_PIL)
    # オリジナルとキャンパスを合成して保存
    result = Image.alpha_composite(src_image_PIL, tmp)

    return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)

def overlay_faces(src_image, ol_image, faces, writeID = False):
    # 戻り値とする変数
    dst_image = src_image
        
    # 認識した顔に画像を上乗せする
    for i in range(0,len(faces)):

        # 扱いやすいように変数を用意
        tmpCoord = faces[i].coordinate
        tmpId = faces[i].id
        
        # 認識範囲にあわせて画像をリサイズ
        resized_ol_image = resize_image(ol_image, tmpCoord[2], tmpCoord[3])
        
        print("認識した顔の数(ID) = "+str(tmpId))
        
        # 特定のidのみ顔を上書き
        if True:#tmpId < 20 :
        
            # オーバレイ画像の作成
            dst_image = overlay(dst_image, resized_ol_image, [tmpCoord[0]+tmpCoord[2]/2,tmpCoord[1]+tmpCoord[3]/2])
        
            if writeID:
                # 顔のIDを書き込み
                cv2.putText(dst_image,str(tmpId),(tmpCoord[0],tmpCoord[1]),cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0))

    return dst_image

if __name__ == '__main__':
    movie_overlay3()