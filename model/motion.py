
import cv2
import pickle
import flask
import numpy as np

class motiondetector:
    frames = []

    def predict(self,data):
        self.frames = data
        if not len(self.frames):
            return 0
        frame1 = np.array(self.frames[0],dtype= np.uint8)
        # frame1 = np.reshape(frame1, (200,200,3))
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

        for fr in  self.frames[1:]:
            frame = np.array(fr,dtype= np.uint8)
            # frame = np.reshape(frame, (200,200,3))
            gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
            
            deltaframe=cv2.absdiff(gray1,gray2)
            threshold = cv2.threshold(deltaframe, 25, 255, cv2.THRESH_BINARY)[1]
            threshold = cv2.dilate(threshold,None)

            countour,heirarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for i in countour:
                if cv2.contourArea(i) < 10000:
                    continue
                else:
                    (x, y, w, h) = cv2.boundingRect(i)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    return 1
        return 0


def predict(image):
    obj = motiondetector()
    res  = str(obj.predict(image))
    return res