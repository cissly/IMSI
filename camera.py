
import cv2
import numpy as np
from time import sleep
from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.

#face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

while True:
    im = picam2.capture_array()

    #print("aa:",np.array(im).shape)
    img_hsv=cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    #print("bb:",np.array(img_hsv).shape)


    lower_red = np.array([0,50,50]) #example value
    upper_red = np.array([10,255,255]) #example value
    mask = cv2.inRange(img_hsv, lower_red, upper_red)

    # print("cc:",np.array(mask).shape)
    
    # print(np.sum(mask[:,:320]))

    # print(np.sum(mask[:,320:]))


    dst = im.copy()
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(gray,5000,1500,apertureSize=5,L2gradient=True)
    
    lines = cv2.HoughLinesP(canny,0.8,np.pi / 180,90,minLineLength=10,maxLineGap=100)
    
    #print(type(lines))
    if type(lines) == type(None):
        pass
    else:
        for i in lines:
            cv2.line(dst,(int(i[0][0]), int(i[0][1])), (int(i[0][2]),int(i[0][3])),(0,0,225),2)
        print("i",i)

    img_result = cv2.bitwise_and(im, im, mask=mask)
    dif = np.sum(mask[:,:320]) - np.sum(mask[:,320:])

    #print("dif :", dst)
    # if -100 <= dif and dif <= 100:
    #     print("go")
    # elif dif > 100:
    #     print( "left")
    # else:
    #     print("right")
    # sleep(1)

    numpy_img = np.array(img_result)
    #print(numpy_img)

    #print(np.array(img_result).shape)
    cv2.imshow("Camera", dst)
    cv2.waitKey(1)
# camera_config = picam2.create_preview_configuration()
# picam2.configure(camera_config)
# picam2.start_preview(Preview.QTGL)
# picam2.start()
# time.sleep(2)
# picam2.capture_file("test.jpg")

# import cv2
# cap = cv2.VideoCapture(0)
# #cap  = cv2.VideoCapture(f'v412src device=/dev/video0 io-mode=2 ! image/jpeg, width=(int)380, height(int),240 ! nvjpegdec ! video/x-raw, format=I420 ! appsink',cv2.CAP_GSTREAMER)
# try :
#     while True:
#         ret,frame = cap.read()
#         if not ret:
#             print("nooo")
#             break
#         frame = cv2.resize(frame,(320,240))

#         cv2.imshow("frame",frame)
# except KeyboardInterrupt:
#     print("finish")

# finally:
#     cap.release()
#     cv2.destroyAllWindows()
