from filecmp import dircmp
from PIL import Image
from io import BytesIO
from kafka import KafkaConsumer
from flask import Flask,request,jsonify
import numpy as np
import json
import cv2
# from emotion_detection import *
# import face_model
consumer = KafkaConsumer("m_kp_1",bootstrap_servers=['52.140.63.83:9092'])

for message in consumer:
        print("Message Recieved")
        # print(message.value)
        # stream = BytesIO(message.value)


        # # # print("dict:\n",dict['b'])
        # # print("Stream:", type(stream.getvalue()))
        # # image = Image.open(stream).convert("RGB")
        # # frame = np.array(image)
        # # # print("type: ", type(i))
        
        # # # print(image.shape)
        # # stream.close()
        # # image.show()
        
        # # # Converted numpy array to List to send it through JSOn
        # # a = frame.tolist()
        # # dict_a = {

        # #     'b': a
        # # }

        # # print(dict_a)