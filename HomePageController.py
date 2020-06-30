import sys
sys.path.insert(1, './change_background')
from change_back import driver
import cv2
sys.path.insert(1, './View')
from View import HomePageView
sys.path.insert(1, './Model')
from Model import Client
import time
import threading as Thread
from PyQt5 import QtCore
import sys


class HomePage_Controller():
    def __init__(self):
        self.user_image_data = None
        # self.take_shot(self.callback)
        self.take_shot_from_webcam(self.callback)
        self.window = None
    def take_shot(self, callback=None):
        processed_img = driver('User_Image.png','./change_background/images')
        isProcessing = True
        while isProcessing:
            print("process")
            if processed_image != None:
                print("received processed image")
                callback('User_Image.png')
                isProcessing = False 
    def callback(self,imageFileName):
        print(imageFileName)
        with open(imageFileName, 'rb') as fp:
            print("open")
            image_data = fp.read()
        print("opened")
        assert(len(image_data))
        print("imagedata")
        self.user_image_data = image_data
        self.navigate_to_homepage(image_data)
        # self.connect_to_socket(image_data)
    def callback_from_hmpage(self,window,user_image_data):
        print("bargasht baba")
        self.window = window
        background = MyThread(window , user_image_data)
        t = Thread.Thread(target=background.process)
        t.start()
        background.notify.connect(self.notify)
        # background.notify.connect(self.notify)
    def navigate_to_homepage(self,user_image_data):
        print("yes")
        HomePageView.main(user_image_data,self.callback_from_hmpage)
    # @QtCore.pyqtSlot()
    def notify(self,data,client_number):
        print("I have been notified",len(data))
        self.window.update_ui(data,client_number)
    def take_shot_from_webcam(self,callback = None):
        cap = cv2.VideoCapture(0)
        # Check if the webcam is opened correctly
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        while True:
            ret, frame = cap.read()
            img_counter = 0
            # try:
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Input', frame)
            c = cv2.waitKey(1)
            if c == 27:
                break
            elif c == 32:
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                if callback:
                    cap.release()
                    cv2.destroyAllWindows()
                    callback(img_name)
                    break
                img_counter += 1
            # except:
            # print("no access")
        cap.release()
        cv2.destroyAllWindows()
class MyThread(QtCore.QObject):

    notify = QtCore.pyqtSignal(bytes,int)
    def __init__(self, parent,user_image_data):
        print("thread")
        super(MyThread, self).__init__(parent)
        print("thread1")
        self.should_continue = True
        self.user_image_data = user_image_data
        self.other_client_data = None
    def callback(self,data,client_number):
        self.notify.emit(data,client_number)
    def process(self):
        while self.should_continue:
            print("should countinue")
            print(len(self.user_image_data))
            self.connect_to_socket(self.user_image_data)
            # Here, do your server stuff.
    def connect_to_socket(self,user_image_data):
        print("socket is connecting")
        Client.main(user_image_data,self.callback)
    
if __name__ == "__main__":
    hm_p = HomePage_Controller()