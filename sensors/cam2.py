from kafka import KafkaProducer
from time import sleep
import cv2
while(True):
    producer=KafkaProducer(bootstrap_servers=['52.140.63.83:9092'])
    image = cv2.imread("images/collage.jpg")
    ret, buffer = cv2.imencode('.jpg', image)
    producer.send("cam2",buffer.tobytes())
    sleep(20)