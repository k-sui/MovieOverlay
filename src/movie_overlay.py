#coding=utf-8

'''
Created on 2016/01/31

@author: master
'''

import cv2
import datetime
import numpy as np
from PIL import Image

def movie_overlay():

    target = "../target/smile.mp4"
    result = "../result/smile_recog.m4v" 
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # 顔認識用特徴量のファイル指定
    cascade_path = "C:/Development/Anaconda2/Library/etc/haarcascades/haarcascade_frontalface_alt.xml"
    #　認識した顔の色を指定。ここでは白。
    color = (255, 255, 255) 

    movie = cv2.VideoCapture(target)    
    out = cv2.VideoWriter(result, fourcc, 23.0, (1920,1080))
    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)

    # オーバーレイ画像の読み込み
    ol_imgae_path = "../target/warai_otoko.png"    
    ol_image = cv2.imread(ol_imgae_path,cv2.IMREAD_UNCHANGED)
    
    
    count = 0
    
    while movie.isOpened():
        
        ret,frame = movie.read()

        #image_path = "../result/smile"+str(count)+".png"
        #cv2.imwrite(image_path, frame)

#        if ret:
        if ret and count > -1 and count < 120 :
            # グレースケールに変換
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 顔認識の実行
            facerecog = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

            if len(facerecog) > 0:
                # 認識した顔に画像を上乗せする
                for rect in facerecog:

                    # 認識範囲にあわせて画像をリサイズ
                    resized_ol_image = resize_image(ol_image, rect[2], rect[3])
                    
                    # オーバレイ画像の作成
                    frame = overlay(frame, resized_ol_image, [rect[0]+rect[2]/2,rect[1]+rect[3]/2])
        #            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
    
            out.write(frame)
            if count%10 == 0:
                d = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print d + '   現在フレーム数：'+str(count)
        elif count > 120 :
            break
        
        count += 1

    print "出力フレーム数："+str(count)
    

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

#    cv2.imwrite("../result/src_tmp0.png", src_image)
#    cv2.imwrite("../result/overlay_tmp0.png", overlay_image)

    # OpenCVの画像データをPILに変換
    
    #　BGRAからRGBAへ変換
#    src_image_RGB = src_image[::-1, :, ::-1].copy()
#    overlay_image_RGB = overlay_image[::-1, :, ::-1].copy()
    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    overlay_image_RGBA = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)
    
#    cv2.imwrite("../result/src_tmp1.png", src_image_RGBA)
#    cv2.imwrite("../result/overlay_tmp1.png", overlay_image_RGBA)
    
    #　PILに変換
    src_image_PIL=Image.fromarray(src_image_RGBA)
    overlay_image_PIL=Image.fromarray(overlay_image_RGBA)

#    src_image_PIL.save("../result/src_tmp2.png")
#    overlay_image_PIL.save("../result/overlay_tmp2.png")
 
    # 合成のため、RGBAモードに変更
    src_image_PIL = src_image_PIL.convert('RGBA')
    overlay_image_PIL = overlay_image_PIL.convert('RGBA')

#    src_image_PIL.save("../result/src_tmp3.png")
#    overlay_image_PIL.save("../result/overlay_tmp3.png")
 
    # 同じ大きさの透過キャンパスを用意
    tmp = Image.new('RGBA', src_image_PIL.size, (255, 255,255, 0))
    # rect[0]:x, rect[1]:y, rect[2]:width, rect[3]:height
    # 用意したキャンパスに上書き
    tmp.paste(overlay_image_PIL, (coordinate[0]-ol_height/2, coordinate[1]-ol_width/2), overlay_image_PIL)
    # オリジナルとキャンパスを合成して保存
    result = Image.alpha_composite(src_image_PIL, tmp)

#    result.save("../result/result_tmp2.png")
    
    return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)
        
if __name__ == '__main__':
    movie_overlay()