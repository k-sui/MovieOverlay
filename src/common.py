# -*- coding:utf-8 -*-

'''
Created on 2016/01/31

@author: master
'''

import cv2
import numpy as np
from PIL import Image

# PIL���g���ĉ摜������
def overlayOnPart(src_image, overlay_image, posX, posY, zoom):

    # �I�[�o���C�摜��{���ɍ��킹�Ċg��k��
    resized_overlay_image = resize_image(overlay_image, zoom)

    # �I�[�o���C�摜�̃T�C�Y���擾
    ol_height, ol_width = resized_overlay_image.shape[:2]

    # OpenCV�̉摜�f�[�^��PIL�ɕϊ�
    
    #�@BGRA����RGBA�֕ϊ�
    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    resized_overlay_image_RGBA = cv2.cvtColor(resized_overlay_image, cv2.COLOR_BGRA2RGBA)
    
    #�@PIL�ɕϊ�
    src_image_PIL=Image.fromarray(src_image_RGBA)
    resized_overlay_image_PIL=Image.fromarray(resized_overlay_image_RGBA)

    # �����̂��߁ARGBA���[�h�ɕύX
    src_image_PIL = src_image_PIL.convert('RGBA')
    resized_overlay_image_PIL = resized_overlay_image_PIL.convert('RGBA')

    # �����傫���̓��߃L�����p�X��p��
    tmp = Image.new('RGBA', src_image_PIL.size, (255, 255,255, 0))
    # rect[0]:x, rect[1]:y, rect[2]:width, rect[3]:height
    # �p�ӂ����L�����p�X�ɏ㏑��
    tmp.paste(resized_overlay_image_PIL, (int(posX-ol_height/2), int(posY-ol_width/2)), resized_overlay_image_PIL)
    # �I���W�i���ƃL�����p�X���������ĕۑ�
    result = Image.alpha_composite(src_image_PIL, tmp)

    return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)

               
def resize_image(image, zoom):
    
    # ���X�̃T�C�Y���擾
    org_height, org_width = image.shape[:2]

    ratio = float(zoom)/100
    
    # �傫�����̃T�C�Y�ɍ��킹�ďk��
    resized = cv2.resize(image,(int(org_width*ratio),int(org_height*ratio)))
    
    return resized    