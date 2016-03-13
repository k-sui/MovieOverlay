#coding=utf-8
'''
Created on 2016/02/03

@author: master
'''

import numpy as np

class FacePosition:
    '''
    
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
    
    faceCount = 0

    def __init__(self, frame, coordinates):

        '''
        フレームと認識した顔の座標・サイズを渡す。
        顔の数分だけFacePointクラスのインスタンスを作成
        '''

    # 今まで何番までidを割り振ったかを記録
        self.faces = [None]*len(coordinates)

        self.frame = frame
        for i in range(0, len(coordinates)):
#            if initialize:
#                self.faces[i] = FacePoint(self.face_count, coordinates[i])
#                self.face_count += 1
#            else:
#                self.faces[i] = FacePoint(-1, coordinates[i])
#
            self.faces[i] = FacePosition(FaceFrame.faceCount, coordinates[i])
            FaceFrame.faceCount += 1

    def append(self, faceId, coordinate):
        self.faces.append(FacePosition(faceId, coordinate))

class FrameManager:
    
    LIST_SIZE = 5
    CENTER_INDEX = 2
    # フレーム間の顔が同じ顔であるかを判断する際の、位置、サイズの差をどこまで認めるか。%で指定
    ALLOWED_GAP = 10
    
    FRAME_HEIGHT = 1080
    FRAME_WEDTH  = 1920
    
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.__frames = [None]*self.LIST_SIZE
        
    
    def put(self, frame, coordinates):
        # 一番最初のフレームの場合(framesが定義されていない状態の場合)、フレームに初期IDを振る。
        if frame is None:
            faceFrame = None
        else:
            faceFrame = FaceFrame(frame, coordinates)

        # 保存しているフレーム数がLIST_SIZE以下の場合、最後尾にフレームを追加する
#        if __frames is None:
#            __frames[0] = FaceFrame(frame, coordinates))
            
#        elif len(frames) < LIST_SIZE :
#            __frames[len(__frames)] = FaceFrame(frame, coordinates))
            
        # 保存しているフレーム数がLIST_SIZEの場合、先頭を削除して末尾に追加
#        else:
        # リストを1つづつ前にずらし、最後尾に引数のフレームを追加する。全パターンこれでいけそう
        returnFrame = self.__frames[0]
        for i in range(0,len(self.__frames)-1):
            self.__frames[i] = self.__frames[i+1]
        self.__frames[FrameManager.LIST_SIZE-1] = faceFrame

        # 前後のフレームから連続性を確認する
        # CENTER_INDEXの前後それぞれの組み合わせ
        for i in range(0, FrameManager.CENTER_INDEX):
            for j in range(FrameManager.CENTER_INDEX+1, FrameManager.LIST_SIZE):
                if self.__frames[i] is not None and self.__frames[FrameManager.CENTER_INDEX] is not None and self.__frames[j] is not None:
                    #self.connectFaces(self.__frames[i].faces, self.__frames[FrameManager.CENTER_INDEX].faces, self.__frames[j].faces)
                    self.connectFaces(self.__frames[i], self.__frames[FrameManager.CENTER_INDEX], self.__frames[j])

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
                
            # 後のフレームで認識された顔に同じ顔がある場合、その顔も間のフレームにあるものとして補完する。
            if matched == False:
                for k in range(0, backFaceNum):
                    if self.compare(frameF.faces[i], frameB.faces[k]):
                        frameC.append(frameF.faces[i].id, ((frameF.faces[i].coordinate + frameB.faces[k].coordinate)/2).astype(np.int))
                        # 顔の数を1増やす。(あとの処理でもう1つ顔が見つかった場合のため)
                        centerFaceNum += 1
                        if(centerFaceNum>10):
                            break


        
    def compare(self, face1, face2):
        
        result = True
        for i in range(0,4):
            if i%2 == 0:
                gap = ((float(face1.coordinate[i])-float(face2.coordinate[i]))/FrameManager.FRAME_HEIGHT)*100
            else:
                gap = ((float(face1.coordinate[i])-float(face2.coordinate[i]))/FrameManager.FRAME_WEDTH)*100
            if (-1*FrameManager.ALLOWED_GAP < gap < FrameManager.ALLOWED_GAP) == False:
                result = False
                break
        return result
                    
