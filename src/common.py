# -*- coding:utf-8 -*-

'''
Created on 2016/01/31

@author: master
'''

import cv2
import numpy as np
from PIL import Image

# PILを使って画像を合成
def overlayOnPart(src_image, overlay_image, posX, posY, zoom):

    # オーバレイ画像を倍率に合わせて拡大縮小
    resized_overlay_image = resize_image(overlay_image, zoom)

    # オーバレイ画像のサイズを取得
    ol_height, ol_width = resized_overlay_image.shape[:2]

    # OpenCVの画像データをPILに変換
    
    #　BGRAからRGBAへ変換
    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    resized_overlay_image_RGBA = cv2.cvtColor(resized_overlay_image, cv2.COLOR_BGRA2RGBA)
    
    #　PILに変換
    src_image_PIL=Image.fromarray(src_image_RGBA)
    resized_overlay_image_PIL=Image.fromarray(resized_overlay_image_RGBA)

    # 合成のため、RGBAモードに変更
    src_image_PIL = src_image_PIL.convert('RGBA')
    resized_overlay_image_PIL = resized_overlay_image_PIL.convert('RGBA')

    # 同じ大きさの透過キャンパスを用意
    tmp = Image.new('RGBA', src_image_PIL.size, (255, 255,255, 0))
    # rect[0]:x, rect[1]:y, rect[2]:width, rect[3]:height
    # 用意したキャンパスに上書き
    tmp.paste(resized_overlay_image_PIL, (int(posX-ol_height/2), int(posY-ol_width/2)), resized_overlay_image_PIL)
    # オリジナルとキャンパスを合成して保存
    result = Image.alpha_composite(src_image_PIL, tmp)

    return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)

               
def resize_image(image, zoom):
    
    # 元々のサイズを取得
    org_height, org_width = image.shape[:2]

    ratio = float(zoom)/100
    
    # 大きい方のサイズに合わせて縮小
    resized = cv2.resize(image,(int(org_width*ratio),int(org_height*ratio)))
    
    return resized    