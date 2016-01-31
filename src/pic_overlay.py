#coding=utf-8

'''
Created on 2016/01/30


@author: master
'''

import cv2
import numpy as np
from PIL import Image


def pic_overlay():

    # 顔認識用特徴量のファイル指定
    cascade_path = "C:/Development/Anaconda2/Library/etc/haarcascades/haarcascade_frontalface_alt.xml"
    
    # 認識対象ファイルの読み込み
    image_path = "../target/Lenna.png"
    image = cv2.imread(image_path,cv2.IMREAD_UNCHANGED)

    # オーバーレイ画像の読み込み
    ol_imgae_path = "../target/warai_otoko.png"    
    ol_image = cv2.imread(ol_imgae_path,cv2.IMREAD_UNCHANGED)
    
    # グレースケールに変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    
    #物体認識（顔認識）の実行
    #image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
    #objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
    #scaleFactor – 各画像スケールにおける縮小量を表します
    #minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
    #flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
    #minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
    
    # 顔認識の実行
    facerecog = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
    
    # 認識結果を表示
    print "認識した場所は"
    print facerecog
    
    if len(facerecog) > 0:
        # 認識した顔全てを矩形で囲む
        for rect in facerecog:
            
            # 認識範囲にあわせて画像をリサイズ
            resized_ol_image = resize_image(ol_image, rect[2], rect[3])
            
            # オーバレイ画像の作成
            image = overlay2(image, resized_ol_image, [rect[0]+rect[2]/2,rect[1]+rect[3]/2])
#            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
    
        # 認識結果の出力
        # cv2.imwrite("../result/Lenna_result.jpg", image)
        cv2.imwrite("../result/Lenna_result.jpg", image)
    
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

# 中心座標を指定
def overlay(src_image, overlay_image, coordinate):
    
    # オーバレイ画像のサイズを取得
    ol_height, ol_width = overlay_image.shape[:2]
    
    # アルファチャンネルの抽出
    alpha = overlay_image[:,:,3]
    # RGBの3色分に複製
    alpha = cv2.cvtColor(alpha, cv2.COLOR_GRAY2BGR)
    # 後の計算のために0.0-1.0の範囲に
    alpha = alpha / 255.0
    
    # アルファチャンネルの除去
    overlay_image = overlay_image[:,:,:3]
    
    pt = [coordinate[0]-ol_height/2, coordinate[1]-ol_width/2, coordinate[0]+ol_height/2, coordinate[1]+ol_width/2]
    
    print pt
    
    # 重ね合わせる先の画像から、透過率分の色を減らす
#    src_image[pt[0]:pt[2]:, pt[1]:pt[3]] *= 1.0 - alpha  # 透過率に応じて元の画像を暗くする。
#    src_image[pt[0]:pt[2]:, pt[1]:pt[3]] += overlay_image * alpha
    print src_image.shape
    print overlay_image.shape
    src_image[pt[0]:pt[2]:, pt[1]:pt[3]] *= 1  # 透過率に応じて元の画像を暗くする。
    src_image[pt[0]:pt[2]:, pt[1]:pt[3]] += overlay_image
    
    return src_image
    
# PILを使って画像を合成
def overlay2(src_image, overlay_image, coordinate):

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
    
    return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGRA)
        
if __name__ == '__main__':
    pic_overlay()