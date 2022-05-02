import cv2
from time import sleep
from kafka import KafkaProducer
from flask import Flask
import sys
import numpy as np
from PIL import Image
app = Flask(__name__)

cap = cv2.VideoCapture(0)
# kafka_server = sys.argv[1]
# topic_name = sys.argv[2]
kafka_server = '52.140.63.83:9092'
topic_name='cam71'
i=0
producer = KafkaProducer(bootstrap_servers=[kafka_server])
dim = (200,200)
while(1):
  vid = list()
  data = cap.read()[1]
  print("Data Shape: ", data.shape)
  ret, buffer = cv2.imencode('.jpeg', data)
  # a = data.tobytes()
  producer.send(topic_name, buffer.tobytes())

  # if i%2 == 1:
  #   image = cv2.imread("cg1.jpeg")
    
  #   # image = cv2.resize(image, dim)
  #   # print("Img 1: ",image.shape)
  #   ret, buffer = cv2.imencode('.jpeg', image)
  #   print("Img 1 a: ",buffer.shape)
  #   a = buffer.tobytes()
  #   # print("Img 1 a: ",a.shape)
  #   producer.send(topic_name, buffer.tobytes())
  #   data = np.frombuffer(a, dtype=buffer.dtype)
  #   print("Img 1 data: ",data.shape)
  #   i=0
  # else:
  #   image = cv2.imread("bill.jpg")

  #   # image = cv2.resize(image, dim)
  #   # print("Img 2: ",image.shape)
  #   ret, buffer = cv2.imencode('.jpg', image)
  #   print("Img 2 a: ",buffer.shape)
  #   a = buffer.tobytes()
    
  #   producer.send(topic_name, buffer.tobytes())
  #   data = np.frombuffer(a, dtype=buffer.dtype)
  #   print("Img 2 data: ",data.shape)
  #   i=1
  sleep(1)

if __name__ == '__main__':
	app.run(debug=True, port=5006)
