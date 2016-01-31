#coding=utf-8

'''
Created on 2016/01/23

@author: master
'''

import cv2

# 顔認識用特徴量のファイル指定
cascade_path = "C:/Development/Anaconda2/Library/etc/haarcascades/haarcascade_frontalface_alt.xml"

# 認識対象ファイルの指定
# image_path = "../target/Lenna.png"
image_path = "../target/ameniodoreba2.png"
# 認識対象ファイルの読み込み
image = cv2.imread(image_path)

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

#　認識した顔の色を指定。ここでは白。
color = (255, 255, 255) 

if len(facerecog) > 0:
    # 認識した顔全てを矩形で囲む
    for rect in facerecog:
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)

    # 認識結果の出力
    # cv2.imwrite("../result/Lenna_result.jpg", image)
    cv2.imwrite("../result/ameniodoreba2.png", image)
