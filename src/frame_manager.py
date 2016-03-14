#coding=utf-8
'''
Created on 2016/02/03

@author: master
'''

import numpy as np

class FacePosition:
    '''
    顔の位置とIDをセットで保持するためのクラス
    IDと座標を顔の座標・サイズを持つただの構造体
    '''

    def __init__(self, id, coordinate):
        '''
        Constructor
        '''
        self.id = id
        self.coordinate = coordinate
        


class FaceFrame:
    '''
    各フレームで認識した顔を保持するためのクラス
    faceCountはアプリケーション全体でIDが被らないように使ったIDの数をカウントするための変数なので、
    使うときは必ずFaceFrame.faceCountでアクセスする
    '''
    
    faceCount = 0

    def __init__(self, frame, coordinates):

        '''
        フレームと認識した顔の座標・サイズを渡す。
        顔の数分だけFacePointクラスのインスタンスを作成
        coodinates: 顔認識結果の配列。cascade.detectMultiScaleの結果をそのまま渡す
        '''
        
        # 顔の数分配列を確保
        self.faces = [None]*len(coordinates)
        self.frame = frame

        # 渡された顔それぞれにidを割り振り、FacePositionのインスタンスを作成
        for i in range(0, len(coordinates)):
            self.faces[i] = FacePosition(FaceFrame.faceCount, coordinates[i])
            FaceFrame.faceCount += 1

    # フレーム内の顔を後から追加するための関数
    def append(self, faceId, coordinate):
        self.faces.append(FacePosition(faceId, coordinate))

class FrameManager:
    
    '''
    渡されたフレームと顔認識結果を元に顔の連続性と抜けた顔の補完を行うクラス
    連続している顔には同じIDを割り振る。
    LIST_SIZE: いくつのFaceFrameを元に顔の連続性を確認するかを指定

    '''

    LIST_SIZE = 5
    CENTER_INDEX = int(LIST_SIZE/2)
    # フレーム間の顔が同じ顔であるかを判断する際の、位置、サイズの差をどこまで認めるか。%で指定
    ALLOWED_GAP = 10
    
    
    def __init__(self, height, width):
        '''
        扱う動画の高さ、幅を指定する
        '''
        FrameManager.FRAME_HEIGHT = height
        FrameManager.FRAME_WIDTH = width

        self.__frames = [None]*self.LIST_SIZE
        
    
    def put(self, frame, coordinates):
        '''
        渡されたフレームと顔認識結果を元にフレームを追加する
        追加時にIDの割り振り、連続性確認、抜けた顔の補完をし、LIST_SIZE番目のFaceFrameのインスタンスを返す
        終了時の処理として、全てのフレームを処理し終えた後、LIST_SIZE個のフレームがFrameManager内に残るので、残ったフレームを出し終えるまで、Noneを追加し続けること。

        return: FaceFrameのインスタンス。但し、LIST_SIZE番目にFaceFrameインスタンスがない場合はNoneを返す。
        '''
        # 一番最初のフレームの場合(framesが定義されていない状態の場合)、フレームに初期IDを振る。
        if frame is None:
            faceFrame = None
        else:
            faceFrame = FaceFrame(frame, coordinates)

        # リストを1つづつ前にずらし、最後尾に引数のフレームを追加する。内部処理にランダムアクセスが多いので配列で管理する方が望ましいと思う。
        returnFrame = self.__frames[0]
        for i in range(0,len(self.__frames)-1):
            self.__frames[i] = self.__frames[i+1]
        self.__frames[FrameManager.LIST_SIZE-1] = faceFrame

        # 前後のフレームから連続性を確認する
        # CENTER_INDEXを境にその前(i)後(j)それぞれの組み合わせで顔の連続性を確認する
        for i in range(0, FrameManager.CENTER_INDEX):
            for j in range(FrameManager.CENTER_INDEX+1, FrameManager.LIST_SIZE):
                # Noneの部分は飛ばす
                if self.__frames[i] is not None and self.__frames[FrameManager.CENTER_INDEX] is not None and self.__frames[j] is not None:

                    # 間にあるフレーム全てに連続性確認、補完を行う
                    for k in range(i+1, j):
                        self.connectFaces(self.__frames[i], k, self.__frames[j])

        return returnFrame
        
        
    def connectFaces(self, frameF, frameC, frameB):

                
        # frameF.facesとframeC.facesで連続している顔があれば同じidを振る。　
        # TODO 同じidが複数の顔に振られうる可能性がある。そもそもこの場合だと今の設計ではうまくいかないので一旦放置。
        frontFaceNum = len(frameF.faces)
        centerFaceNum = len(frameC.faces)
        backFaceNum = len(frameB.faces)
        for i in range(0, frontFaceNum):
            # 前のフレームの中のi番目の顔が間の顔の中のどれかと合致したかを保持
            matched = False
            for j in range(0, centerFaceNum):
                # 同じ顔と判断したら連番にする
                if self.compare(frameF.faces[i], frameC.faces[j]) == True:
                    frameC.faces[j].id = frameF.faces[i].id
                    matched = True
                    break
                
            # frameCに無くてもframeFとframeBの両方にある場合は間のframCにもその顔があるとみなして補完する。
            if matched == False:
                for k in range(0, backFaceNum):
                    if self.compare(frameF.faces[i], frameB.faces[k]):
                        # frameFとframeBの中間の位置・サイズに顔を追加する
                        frameC.append(frameF.faces[i].id, ((frameF.faces[i].coordinate + frameB.faces[k].coordinate)/2).astype(np.int))
                        # 顔の数を1増やす。(あとの処理でもう1つ顔が見つかった場合のため)
                        centerFaceNum += 1

                        # 無限ループ防止
                        if(centerFaceNum>10):
                            break


        
    def compare(self, face1, face2):
        '''
        face1、face2が連続したものであるか比較する。
        return: 同じならTrue、違えばFalse
        '''
        result = True
        # 座標、顔のサイズの違いが誤差の範囲に収まるかを確認し、全て誤差(ALLOWED_GAP)内であれば同じ顔であると判断する
        for i in range(0,4):
            if i%2 == 0:
                gap = ((float(face1.coordinate[i])-float(face2.coordinate[i]))/FrameManager.FRAME_HEIGHT)*100
            else:
                gap = ((float(face1.coordinate[i])-float(face2.coordinate[i]))/FrameManager.FRAME_WIDTH)*100
            if (-1*FrameManager.ALLOWED_GAP < gap < FrameManager.ALLOWED_GAP) == False:
                result = False
                break
        return result
                    
