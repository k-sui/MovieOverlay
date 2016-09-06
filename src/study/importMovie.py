#coding=utf-8

'''
Created on 2016/01/30

@author: master
'''

import cv2

def cut_movie():

    movie = cv2.VideoCapture("../target/fafner.mp4")

    for i in range(10):
        if movie.isOpened() == False:
            break
        
        ret,frame = movie.read()
        #cv2.imshow("Camera Test",frame)
        filepath = "../result/fafner"+str(i)+".png"
        cv2.imwrite(filepath, frame)
        

if __name__ == '__main__':
    cut_movie()