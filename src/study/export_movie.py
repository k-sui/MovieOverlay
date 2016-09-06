#coding=utf-8

'''
Created on 2016/01/30

@author: master
'''

import cv2

def export_movie():


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
   
    # 最初の1フレームを読み込む
    if movie.isOpened() == True:
        ret,frame = movie.read()
    else:
        ret = False

    # フレームの読み込みに成功している間フレームを書き出し続ける
    while ret:
        
        # 読み込んだフレームを書き込み
        out.write(frame)

        # 次のフレームを読み込み
        ret,frame = movie.read()


if __name__ == '__main__':
    export_movie()