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
    updatelock = False # トラックバー処理中のロックフラグ
    windowname = 'frame' # Windowの名前
    trackbarname = 'Position' # トラックバーの名前


    def __init__(self, params):
        '''
        Constructor
        '''
        