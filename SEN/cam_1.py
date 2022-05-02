import cv2
from time import sleep
from kafka import KafkaProducer
from flask import Flask
import sys
import numpy as np
app = Flask(__name__)

# kafka_server = sys.argv[1]
# topic_name=sys.argv[2]
kafka_server = '52.140.63.83:9092'
topic_name='cam_1'
while(1):
  producer = KafkaProducer(bootstrap_servers=[kafka_server], max_request_size=19801370) # <<<<<< Yaha problem hai, dusari image send ho rhi h pr cg1.jpg nhi ho rhi
  image = cv2.imread("cg1.jpeg")
  ret, buffer = cv2.imencode('.jpeg', image)
  print(buffer.shape)
  # a=buffer.tobytes()
  producer.send(topic_name, buffer.tobytes())
  # data = np.frombuffer(a, dtype=buffer.dtype)
  # print(data.shape)
  sleep(20)

if __name__ == '__main__':
	app.run(debug=True, port=5007)
