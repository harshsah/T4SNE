# __author__ = 'bunkus'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button

import cv2
from gtts import gTTS
import os
import time

import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

import speech_recognition as sr
import pyttsx3 


# Sampling frequency
FREQ = 44100
# Recording duration
DURATION = 7
# Name fof the video file 
VIDEO_FILE_NAME = "video.mp4"
# URL
URL = 'http://192.168.43.1:8080/video' ## Change the url
"""
TYPE = 1 : use all three
TYPE = 2 : use only video and ip-cam
TYPE = 3 : use only video
"""
TYPE = 1


class MainApp(App):

    def build(self):
        self.showVideo = True
        self.img1=Image()
        layout = BoxLayout(orientation ='vertical')
        inner_box = BoxLayout(orientation ='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        button_box = BoxLayout(orientation ='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
        layout.add_widget(self.img1)
        layout.add_widget(inner_box)
        layout.add_widget(button_box)
        self.messageBtn =  Button(text ="App Started",
                        disabled = True,
                        )
        self.typeToggleBtn = Button(text ="Restart",
                        )
        self.typeToggleBtn.bind(on_press = self.typeToggleBtnCallback)
        self.swithcBtn = Button(text ="Switch Cam",
                        )
        self.swithcBtn.bind(on_press = self.switch_camera)
        self.capBtn = Button(text ="Capture",
                        )
        self.capBtn.bind(on_press = self.capBtnCallback)
        inner_box.add_widget(self.messageBtn)
        button_box.add_widget(self.typeToggleBtn)
        button_box.add_widget(self.swithcBtn)
        button_box.add_widget(self.capBtn)
        #opencv2 stuffs
        if TYPE == 1:
            self.camIndex = 0
            self.capture = cv2.VideoCapture(self.camIndex, cv2.CAP_DSHOW)
        else:
            self.camIndex = 1
            self.capture = cv2.VideoCapture(VIDEO_FILE_NAME )
        # cv2.namedWindow("CV2 Image")
        self.clock = Clock.schedule_interval(self.update, 1.0/33.0)
        return layout
    
    def typeToggleBtnCallback(self, event):
        print("restart button pressed")
        # if self.typeToggleBtn.text == "1":
        #     self.typeToggleBtn.text = "2"
        # elif self.typeToggleBtn.text == "2":
        #     self.typeToggleBtn.text = "1"
        self.showVideo = True
        # self.capture =  cv2.VideoCapture(self.camIndex, cv2.CAP_DSHOW)

    def capBtnCallback(self, event):
        print("cap button pressed")

        self.typeToggleBtn.disabled = True
        self.capBtn.disabled = True
        self.swithcBtn.disabled = True

        self.showVideo = False
        # self.capture.release()
        self.messageBtn.text = "Ask Your Question"
        filename = "recording.wav"

        recording = sd.rec(int(DURATION * FREQ), samplerate=FREQ, channels=2)
        sd.wait()
        # write("recording0.wav", freq, recording)
        wv.write(filename, recording, FREQ, sampwidth=2)
        
        r = sr.Recognizer() 
        self.questionText = ''
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            self.questionText = r.recognize_google(audio_data)
            print("The question is: ",self.questionText)
        
        self.messageBtn.text = "Your Question: " + self.questionText

        print("Before time")
        time.sleep(2)
        print("After time")

        answer = self.getAnswer()
        
        self.messageBtn.text += "\nAnswer: " + answer

        engine = pyttsx3.init()
        engine.say(answer)
        engine.runAndWait()

        self.typeToggleBtn.disabled = False
        self.capBtn.disabled = False
        self.swithcBtn.disabled = False
        self.showVideo = True

    def getAnswer(self):
        # result = function(self.frame, self.questionText)
        return self.questionText

    def switch_camera(self, event):
        print("swtich button pressed")
        if TYPE == 1:
            if self.camIndex == 0:
                self.showVideo = False
                del(self.capture)
                self.camIndex = 1
                self.capture = cv2.VideoCapture(VIDEO_FILE_NAME )
            elif self.camIndex == 1:
                self.showVideo = False
                del(self.capture)
                self.camIndex = 2
                self.capture = cv2.VideoCapture(URL)
            elif self.camIndex == 2:
                self.showVideo = False
                del(self.capture)
                self.camIndex = 0
                self.capture = cv2.VideoCapture(self.camIndex, cv2.CAP_DSHOW)
        elif TYPE == 2:
            if self.camIndex == 1:
                self.showVideo = False
                del(self.capture)
                self.camIndex = 2
                self.capture = cv2.VideoCapture(URL)
            elif self.camIndex == 2:
                self.showVideo = False
                del(self.capture)
                self.camIndex = 1
                self.capture = cv2.VideoCapture(VIDEO_FILE_NAME )
        else:
        	pass

        success, frame = self.capture.read()
        if not success:
            if TYPE == 1:
                self.camIndex = 0
                del(self.capture)
                self.capture = cv2.VideoCapture(self.camIndex, cv2.CAP_DSHOW)  
            else:
                self.camIndex = 1
                del(self.capture)
                self.capture = cv2.VideoCapture(VIDEO_FILE_NAME )
        self.showVideo = True 

    def launchChildApp(self, button):
        self.clock.cancel()
        self.update(1.0/33.0, True)
        # self.capture.release()
        # ChildApp().run()

    def update(self, dt, cap=False):
        # display image from cam in opencv window
        if self.showVideo:
            ret, self.frame = self.capture.read()
            frame = self.frame
            # print(frame)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.img1.texture = texture1
        # cv2.imshow("CV2 Image", frame)
        # convert it to texture
        # else:
        #     frame = self.frame

# class ChildApp(App):

#     def build(self):
#         # self.img1=Image(source='image.jpg')
#         layout = BoxLayout(orientation ='vertical')
#         button_box = BoxLayout(orientation ='horizontal', size_hint=(1, None), height=50, pos_hint={'top': 1})
#         # layout.add_widget(self.img1)
#         layout.add_widget(button_box)
#         self.recBtn = Button(text ="Ask Question",
#                         # font_size ="20sp",
#                         # background_color =(1, 1, 1, 1),
#                         # color =(1, 1, 1, 1),
#                         # size =(32, 32),
#                         # size_hint =(1, 0.2),
#                         # pos_hint ={'center_x':.7, 'center_y':.5},
#                         )
#         self.recBtn.bind(on_press = self.callback)
#         button_box.add_widget(self.recBtn)
#         return layout

#     def callback(self, event):
#         print("rec button pressed")
#         print('Yoooo !!!!!!!!!!!')
    



if __name__ == '__main__':
    MainApp().run() 
