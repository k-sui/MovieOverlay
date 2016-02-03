'''
Created on 2016/02/03

@author: master
'''

from queue import Queue
import numpy as np

class FacePoint:
    '''
    classdocs
    '''


    def __init__(self, id, coordinate):
        '''
        Constructor
        '''
        self.id = id
        self.coordinate = coordinate
        


class FaceFrame:
     '''
    classdocs
    '''
    # 今まで何番までidを割り振ったかを記録
    face_count = 0

    def __init__(self, frame, coordinates, initialize = False):

        '''
        フレームと認識した顔の座標・サイズを渡す。
        顔の数分だけFacePointクラスのインスタンスを作成
        '''

        self.frame = frame
        for i in range(0, len(coordinates)):
            if initialize:
                faces[i] = FacePoint(face_count, coordinates[i])
                face_count += 1
            else:
                faces[i] = FacePoint(-1, coordinates[i])
                

class FrameManager:
    
    LIST_SIZE = 5
    CENTER_INDEX = 3
    # フレーム間の顔が同じ顔であるかを判断する際の、位置、サイズの差をどこまで認めるか。%で指定
    ALLOWED_GAP = 3
     '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    
    def put(self, frame, coordinates):
        # 一番最初のフレームの場合(framesが定義されていない状態の場合)、フレームに初期IDを振る。
        if frame is None:
            faceFrame = None
        elif __frames is None:
            faceFrame = FaceFrame(frame, coordinates)

        # 保存しているフレーム数がLIST_SIZE以下の場合、最後尾にフレームを追加する
#        if __frames is None:
#            __frames[0] = FaceFrame(frame, coordinates))
            
#        elif len(frames) < LIST_SIZE :
#            __frames[len(__frames)] = FaceFrame(frame, coordinates))
            
        # 保存しているフレーム数がLIST_SIZEの場合、先頭を削除して末尾に追加
#        else:
        # リストを1つづつ前にずらし、最後尾に引数のフレームを追加する。全パターンこれでいけそう
        returnFrame = __frames[0]
        for i in range(0,LIST_SIZE-1):
            __frames[i] = __frames[i+1]
        __frames[LIST_SIZE-1] = faceFrame

        # 前後のフレームから連続性を確認する
        # CENTER_INDEXの前後それぞれの組み合わせ
        for i in range(0, CENTER_INDEX):
            for j in range(CENTER_INDEX+1, LIST_SIZE):
                if __frames[i] is __frames[CENTER_INDEX] is __frames[j] is not None:
                    connectFaces(__frames[i].faces, __frames[CENTER_INDEX].faces, __frames[j].faces)

        return returnFrame
        
        
    def connectFaces(self, facesF, facesC, facesB):
        
        # facesFとfacesCで連続している顔があれば同じidを振る。　
        # TODO 同じidが複数の顔に振られうる可能性がある。そもそもこの場合だと今の設計ではうまくいかないので一旦放置。
        frontFaceNum = len(faceF)
        centerFaceNum = len(faceC)
        backFaceNum = len(faceB)
        for i in (0, frontFaceNum):
            for j in (0, centerFaceNum):
                # 同じ顔と判断したら連番にする
                if compare(facesF[i], facesC[j]) == True:
                    facesC[j].id = facesF[i].id
                else:
                    # 後のフレームで認識された顔に同じ顔がある場合、その顔も間のフレームにあるものとして補完する。
                    for k in (0, backFaceNum):
                        if compare(facesF[i], facesB[k])
                            facesC[centerFaceNum].id = facesF[i].id
                            facesC[centerFaceNum].coordinate = (facesF[i].coordinate + facesB[i].coordinate)/2
                            # 顔の数を1増やす。(あとの処理でもう1つ顔が見つかった場合のため)
                            centerFaceNum += 1

        
    def compare(self, face1, face2):
        
        result = true
        for i in range(0,4):
            gap = (float(face1.coordinate[0])/float(face2.coordinate[0]) -1)*100
            if -1*ALLOWED_GAP < gap < ALLOWED_GAP:
                result = False
                break
        return result
                    
