#coding=utf-8

'''
Created on 2016/01/23

@author: master
'''

import cv2

# 認識対象ファイルの指定
image_path = "../target/Lenna.png"
# 認識対象ファイルの読み込み
image = cv2.imread(image_path)

# グレースケールに変換
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 顔認識用特徴量のファイル指定
cascade_path = "C:/Development/Anaconda2/Library/etc/haarcascades/haarcascade_frontalface_alt.xml"
# カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)
# 顔認識の実行
facerecog = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

# 認識結果を表示
print ("認識した場所は")
print (facerecog)

#　認識した顔を囲む矩形の色を指定。ここでは白。
color = (255, 255, 255) 

if len(facerecog) > 0:
    # 認識した顔全てを矩形で囲む
    for rect in facerecog:
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)

# 認識結果の出力
cv2.imwrite("../result/Lenna_result.jpg", image)
 