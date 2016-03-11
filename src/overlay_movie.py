#coding=utf-8

'''
Created on 2016/01/31

@author: master
'''

import cv2
import datetime
import numpy as np
from PIL import Image

def overlay_movie():

    # 入力する動画と出力パスを指定。
    target = "target/test_input.mp4"
    result = "result/test_output.m4v" 

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
        
    # 最初の1フレームを読み込む
    if movie.isOpened() == True:
        ret,frame = movie.read()
    else:
        ret = False

    # フレームの読み込みに成功している間フレームを書き出し続ける
    while ret:
        
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
                frame = overlayOnPart(frame, resized_ol_image, rect[0],rect[1])

        # 読み込んだフレームを書き込み
        out.write(frame)

        # 次のフレームを読み込み
        ret,frame = movie.read()

        # 経過を確認するために100フレームごとに経過を出力
        if movie.get(cv2.CAP_PROP_POS_FRAMES)%100 == 0:
            date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            print(date + '  現在フレーム数：'+str(int(movie.get(cv2.CAP_PROP_POS_FRAMES))))

        # 長いので500フレームまでで終了する
        if movie.get(cv2.CAP_PROP_POS_FRAMES) > 500:
            break

    print("完了")
    

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
    overlay_movie()