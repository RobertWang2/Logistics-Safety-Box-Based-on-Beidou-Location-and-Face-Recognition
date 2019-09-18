#encoding=utf-8
import serial
import geocoder
import time
import cv2 as cv
src1=cv.imread('C:\\Users\\LattePanda\\Desktop\\FaceRecognization\\resourses\\image\\success.png')
src2=cv.imread('C:\\Users\\LattePanda\\Desktop\\FaceRecognization\\resourses\\image\\waiting.png')
src3=cv.imread('C:\\Users\\LattePanda\\Desktop\\FaceRecognization\\resourses\\image\\wrong.png')
ser=serial.Serial("COM5",9600,timeout=0.5)
with open('C:\\Users\\LattePanda\\Desktop\\FaceRecognization\\location.txt',mode='r',encoding="utf-8") as f1:
    x=str(f1.readline())
    print(x)
demo=b"0"
while True:
    c=ser.readline()
    c=str(c)
    if(c.count('GNGGA')):
        print(c)
        list=c.split(',')
        NS_value = list[2]
        NS_value_degree = float(NS_value[0:2])
        NS_value_min = float(NS_value[2:9])
        NS_value = NS_value_degree+NS_value_min/60
        NS = list[3]
        if(NS == 'S'):
            NS_value = -NS_value
        print(NS_value)
        EW_value = list[4]
        EW_value_degree = float(EW_value[0:3])
        EW_value_min = float(EW_value[3:10])
        EW_value = EW_value_degree+EW_value_min/60
        EW=list[5]
        if(EW == 'W'):
            EW_value = -EW_value
        print(EW_value)
        print('waiting')
        cv.namedWindow('waiting', cv.WINDOW_NORMAL)
        cv.setWindowProperty('waiting', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.imshow('waiting', src2)
        cv.waitKey(1)
        g = geocoder.arcgis([NS_value,EW_value], method='reverse')
        cv.destroyAllWindows()
        #print(g)
        a=str(g)
        print(a)
        b='<[OK] Arcgis - Reverse ['
        b+=x
        b+=']>'
        print(b)
        if(a==b):
            ser.write(demo)
            print('地点正确')
            cv.namedWindow('success', cv.WINDOW_NORMAL)
            cv.setWindowProperty('success', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            cv.imshow('success', src1)
            cv.waitKey(3000)
            cv.destroyAllWindows()
            break
        if(a!=b):
            print('地点错误')
            cv.namedWindow('wrong', cv.WINDOW_NORMAL)
            cv.setWindowProperty('wrong', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            cv.imshow('wrong', src3)
            cv.waitKey(3000)
            cv.destroyAllWindows()
