#coding=utf-8

'''
Created on 2016/01/30

@author: master
'''

import datetime
import cv2

def face_recognize():

    target = "../target/smile.mp4"
    result = "../result/smile_recog.m4v" 
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # 顔認識用特徴量のファイル指定
    cascade_path = "C:/Development/Anaconda2/Library/etc/haarcascades/haarcascade_frontalface_alt.xml"
    #　認識した顔の色を指定。ここでは白。
    color = (255, 255, 255) 

    movie = cv2.VideoCapture(target)    
    out = cv2.VideoWriter(result, fourcc, 60.0, (1920,1080))
    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    
    count = 0
    
    while movie.isOpened():
        
        ret,frame = movie.read()

        #image_path = "../result/smile"+str(count)+".png"
        #cv2.imwrite(image_path, frame)

#        if ret:
        if ret and count < 100:
            # グレースケールに変換
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 顔認識の実行
            facerecog = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

            if len(facerecog) > 0:
                # 認識した顔全てを矩形で囲む
                for rect in facerecog:
                    cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
            
            out.write(frame)
            if count%10 == 0:
                d = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print(d + '   現在フレーム数：'+str(count))
        else:
            break
        
        count += 1

    print("出力フレーム数："+str(count))
    
if __name__ == '__main__':
    face_recognize()