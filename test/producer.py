from kafka import KafkaProducer
from time import sleep
import cv2
import pickle
producer=KafkaProducer(bootstrap_servers=['52.140.63.83:9092'])
image = cv2.imread("bill.jpg")
print(type(image))

producer.send("m_kp_1",pickle.dumps(image))
sleep(20)