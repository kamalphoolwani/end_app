import cv2
from time import sleep
from kafka import KafkaProducer
from flask import Flask
import sys
import numpy as np
app = Flask(__name__)

kafka_server = sys.argv[1]
topic_name=sys.argv[2]
# kafka_server = '52.140.63.83:9092'
# topic_name='cam_1'
producer = KafkaProducer(bootstrap_servers=[kafka_server], max_request_size=19801370)
while(1):
  image = cv2.imread("cg1.jpeg")
  ret, buffer = cv2.imencode('.jpeg', image)
  print("type: ", type(buffer))
  print(buffer.shape)
  producer.send(topic_name, buffer.tobytes())

  sleep(2)

if __name__ == '__main__':
	app.run(debug=True, port=5007)
