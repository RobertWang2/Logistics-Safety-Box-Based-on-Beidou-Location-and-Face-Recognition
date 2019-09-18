#coding=utf-8
import face_recognition
import cv2 as cv
import threading
from time import ctime,sleep
import os
import geocoder
import time
import pygame
import serial
src = 'C:/Users/LattePanda/Desktop/FaceRecognization/resourses/image/Robert.jpg'
RecognitionMusic = 'recognition.mp3'
WarningMusic = 'warning.mp3'
SuccessMusic = 'face_success.mp3'
SrcMusicPath = 'C:/Users/LattePanda/Desktop/FaceRecognization/resourses/music/'
ser=serial.Serial("COM6",9600,timeout=0.5)
yes=b"1"
no=b"0"
# Get a reference to webcam #0 (the default one)
video_capture = cv.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
src_image = face_recognition.load_image_file(src)
src_face_encoding = face_recognition.face_encodings(src_image)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    src_face_encoding
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
rgb_small_frame = []
face_locations = []
time_start=time.time()
time_end=time.time()

# 1 识别成功 -1识别失败
isTrue = 0
#starttime1 = datetime.datetime.now()
#15 次一秒 在没有识别的情况下
frame = video_capture.read()

def StartMusic(src,des):
    pygame.mixer.init()
    print("播放音乐"+des)
    track = pygame.mixer.music.load(src + des)
    pygame.mixer.music.play(-1)

def StopMusic(des):
    pygame.mixer.music.stop()
    
def location():
    src1=cv.imread('C:\\Users\\LattePanda\\Desktop\\FaceRecognization\\resourses\\image\\success.png')
    src2=cv.imread('C:\\Users\\LattePanda\\Desktop\\FaceRecognization\\resourses\\image\\waiting.png')
    src3=cv.imread('C:\\Users\\LattePanda\\Desktop\\FaceRecognization\\resourses\\image\\wrong.png')
    with open('C:\\Users\\LattePanda\\Desktop\\FaceRecognization\\location.txt',mode='r',encoding="utf-8-sig") as f1:
        x=str(f1.readline())
        print(x)
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
            dict1={b}
            print(dict1)
            dict2={a}
            print(dict2)
            if(a==b):
                print('地点正确')
                cv.namedWindow('success', cv.WINDOW_NORMAL)
                cv.setWindowProperty('success', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                cv.imshow('success', src1)
                cv.waitKey(3000)
                cv.destroyAllWindows()
                return 1
                break
            if(a!=b):
                print('地点错误')
                cv.namedWindow('wrong', cv.WINDOW_NORMAL)
                cv.setWindowProperty('wrong', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                cv.imshow('wrong', src3)
                cv.waitKey(3000)
                cv.destroyAllWindows()


def camera():
    count = 0

    global frame,rgb_small_frame,face_locations,SrcMusicPath,RecognitionMusic,isTrue,time_start
    StartMusic(SrcMusicPath, RecognitionMusic)
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        count += 1
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video

        face_locations = face_recognition.face_locations(rgb_small_frame)

        #Display the results
        for top, right, bottom, left in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
            font = cv.FONT_HERSHEY_DUPLEX
            cv.putText(frame, 'Detecting', (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # ---------------------Test---------------------------
            '''cv.circle(frame, (int((left + right) / 2), int((top + bottom) / 2)), int(abs(top - bottom) / 2),
                       (0, 255, 0), 5)
            line_h = (right - left)
            line_v = (bottom - top)
            cv.line(frame, (int(left + line_h*0.1), int(bottom - line_v*(12/25))), (int(left + line_h*(2/5)), int(bottom - line_v*(1/5))), (0, 255, 0), 5)
            cv.line(frame, (int(left + line_h*(2/5)), int(bottom - line_v*(1/5))),
                     (int(left + line_h * (1.0)), int(bottom - line_v * (2 / 3))), (0, 255, 0), 5)'''

            # ---------------------Test---------------------------
            #识别错误画×
            if isTrue == -1:
                time_end = time.time()
                duringtime = time_end - time_start
                print(duringtime)
                if duringtime <= 3:
                    cv.line(frame, (left, top,), (right, bottom), (0, 0, 255), 5)
                    cv.line(frame, (left, bottom), (right, top), (0, 0, 255), 5)
                else:
                    isTrue = 0
                    time_start = time.time()
            #识别正确画绿色的勾
            if isTrue == 1:
                time_end = time.time()
                duringtime = time_end - time_start
                print(duringtime)
                if duringtime <= 3:
                     cv.circle(frame, (int((left + right) / 2), int((top + bottom) / 2)), int(abs(top - bottom) / 2),
                       (0, 255, 0), 5)
                     line_h = (right - left)
                     line_v = (bottom - top)
                     cv.line(frame, (int(left + line_h*0.1), int(bottom - line_v*(12/25))), (int(left + line_h*(2/5)), int(bottom - line_v*(1/5))), (0, 255, 0), 5)
                     cv.line(frame, (int(left + line_h*(2/5)), int(bottom - line_v*(1/5))),
                     (int(left + line_h * (1.0)), int(bottom - line_v * (2 / 3))), (0, 255, 0), 5)
                else:
                    isTrue = 0
                    time_start = time.time()
        # Display the resulting image
        cv.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # Release handle to the webcam
    video_capture.release()
    cv.destroyAllWindows()

def recognition():
    global frame, rgb_small_frame, face_locations, SrcMusicPath, RecognitionMusic,isTrue
    while True:
        isTrue=0

        sleep(1)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.35)

            # If a match was found in known_face_encodings, just use the first one.
            if True == matches[0]:
                StopMusic(RecognitionMusic)
                StartMusic(SrcMusicPath,SuccessMusic)
                isTrue=1
				
                time_start = time.time()
                cv.waitKey(3000)
                StopMusic(SuccessMusic)
                StartMusic(SrcMusicPath, RecognitionMusic)
            elif matches[0] == False:
                StopMusic(RecognitionMusic)
                StartMusic(SrcMusicPath, WarningMusic)
                # Display the results
                time_start = time.time()
                isTrue=-1
                cv.waitKey(1000)
                StopMusic(SuccessMusic)
                StartMusic(SrcMusicPath, RecognitionMusic)
def main():
    global isTrue
    res = location()
    if res == 1:
        t1 = threading.Thread(target=camera)
        t1.start()
        t2 = threading.Thread(target=recognition)
        t2.start()
        while True:
            if isTrue == 1:
                ser.write(yes)
                print('OK')
            else:
                ser.write(no)
                
				
if __name__ == '__main__':
        main()
