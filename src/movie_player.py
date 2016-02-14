'''
Created on 2016/02/09

@author: master
'''

import numpy as np
import cv2

class MoviePlayer:
    '''
    classdocs
    '''
    __updatelock = False # トラックバー処理中のロックフラグ
    __windowname = 'movieFrame' # Windowの名前
    __trackbarname = 'Position' # トラックバーの名前

    def __init__(self, moviePath):
        '''
        Constructor
        '''
        self.__movie = cv2.VideoCapture(moviePath)
        # 動画の総フレーム数を取得する
        self.__frameNum = int(self.__movie.get(cv2.CAP_PROP_FRAME_COUNT ))
    
    def onTrackbarSlide(self, pos):
        self.__updatelock = True
        self.__movie.set(cv2.CAP_PROP_POS_FRAMES, pos)
        self.__updatelock = False
    
    
    def play(self):
        
        # 名前付きWindowを定義する
        cv2.namedWindow(self.__windowname, cv2.WINDOW_KEEPRATIO|cv2.WINDOW_NORMAL)
        
        # フレーム数が1以上ならトラックバーにセットする
        if (self.__frameNum > 0):
            cv2.createTrackbar(self.__trackbarname, self.__windowname, 0, self.__frameNum, self.onTrackbarSlide)

        # AVIファイルを開いている間は繰り返し（最後のフレームまで読んだら終わる）
        while(self.__movie.isOpened()):
        
            # トラックバー更新中は描画しない
            if (self.__updatelock):
                continue
        
            # １フレーム読む
            ret, frame = self.__movie.read()
        
            # 読めなかったら抜ける
            if ret == False:
                break
        
            # 画面に表示
            cv2.imshow(self.__windowname,frame)
        
            # 現在のフレーム番号を取得
            curpos = int(self.__movie.get(cv2.CAP_PROP_POS_FRAMES))
        
            # トラックバーにセットする（コールバック関数が呼ばれる）
            cv2.setTrackbarPos(self.__trackbarname, self.__windowname, curpos)
        
            # qを押したら抜ける
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # AVIファイルを解放
        self.__movie.release()
        
        # Windowを閉じる
        cv2.destroyAllWindows()
                
if __name__ == '__main__':
    mp = MoviePlayer("../target/smile.mp4")
    mp.play() 
 

        