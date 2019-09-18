import cv2
import face_recognition
import serial

# 基本绘图
# import numpy
cv2.namedWindow("Image")  # 创建窗口
# 抓取摄像头视频图像
cap = cv2.VideoCapture(0)  # 创建内置摄像头变量
src = 'E:/Project/FaceRecognization/resourses/image/Robert.jpg'
des = 'E:/Project/FaceRecognization/resourses/image/unknown.jpg'
ser=serial.Serial("COM3",9600,timeout=0.5)
demo = b"0"

def preprossingSrc(src):
    picture_of_me = face_recognition.load_image_file(src)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
    return my_face_encoding

def recognization(src_encoding,des):

    # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

    unknown_picture = face_recognition.load_image_file(des)

    try:
       unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
    except:
       print('未识别到图像')
       notfound = cv2.imread('E:/Project/FaceRecognization/resourses/image/notfound.jpg')
       cv2.namedWindow('notfound', cv2.WINDOW_AUTOSIZE)
       cv2.resizeWindow("enhanced", 640, 480)
       cv2.imshow('notfound', notfound)
       cv2.waitKey(1000)
       cv2.destroyWindow('notfound')
       return -1
    # Now we can see the two face encodings are of the same person with `compare_faces`!

    try:
        results = face_recognition.compare_faces([src_encoding], unknown_face_encoding,tolerance=0.3)
    except:
        print('未识别到人脸！')

    if results[0] == True:
        print("Correct!")
        #ser.write(demo)
        success = cv2.imread('E:/Project/FaceRecognization/resourses/image/success.jpg')
        cv2.namedWindow('success', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('success', success)
        cv2.waitKey(1000)
        cv2.destroyWindow('success')
        return 1
    else:
        print("Wrong!")
        failed = cv2.imread('E:/Project/FaceRecognization/resourses/image/failed.jpg')
        cv2.namedWindow('failed', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('failed', failed)
        cv2.waitKey(1000)
        cv2.destroyWindow('failed')
        return 0

def camera():
    src_encoding = preprossingSrc(src)
    while (cap.isOpened()):  # isOpened()  检测摄像头是否处于打开状态
        ret, img = cap.read()  # 把摄像头获取的图像信息保存之img变量
        if ret == True:  # 如果摄像头读取图像成功
            cv2.resizeWindow("enhanced", 640, 480)
            cv2.imshow('Image', img)
            k = cv2.waitKey(100)
            if k == ord('a') or k == ord('A') or k == ord('1'):
                cv2.imwrite(des, img)
                res = recognization(src_encoding,des)
                if res == 1:
                    cap.release()  # 关闭摄像头
                    break
    cap.release()  # 关闭摄像头
    #cv2.waitKey(0)
    cv2.destroyWindow('Image')


def main():
    camera()

if __name__ == '__main__':
    main()
