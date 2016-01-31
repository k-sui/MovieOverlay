'''
Created on 2016/01/30

@author: master
'''

import cv2

def copy_movie():
    
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    filepath = "../result/fafner_copy.m4v"

    movie = cv2.VideoCapture("../target/fafner.mp4")    
    out = cv2.VideoWriter(filepath, fourcc, 30.0, (1280,720))
    
    for i in range(100):
        if movie.isOpened() == False:
            break
        
        ret,frame = movie.read()
        #cv2.imshow("Camera Test",frame)
        out.write(frame)

if __name__ == '__main__':
    copy_movie()