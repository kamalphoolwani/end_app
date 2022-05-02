import os
import requests
from kafka import KafkaConsumer
from filecmp import dircmp
from PIL import Image
from io import BytesIO
import numpy as np
import json
import cv2

sensors = dict()
sensor_ids_list = ['1']
sensors['1'] = 'cam_1'
sensors['2'] = 'cam_2'
sensors['3'] = 'cam_3'
sensors['4'] = 'cam71'
sensors['5'] = 'S_1'

url = "http://127.0.0.1:8000"

'''
KAFKA_IP = "52.140.63.83:9092"
motion_consumer = kafka.KafkaConsumer(
bootstrap_servers=[KAFKA_IP]
)

def getsensorkafka(sensor = '1' , num = 20):
    TOPIC = sensors[sensor]
    topic_partition = TopicPartition(TOPIC, 0)
    assigned_topic = [topic_partition]
    consumer.assign(assigned_topic)
    cp = consumer.position(topic_partition)
    consumer.seek(topic_partition,cp-20)
    
'''



def  getsensordata(sensor_id):
	sensor_id = "S_" + str(sensor_id)
	url_ = url + '/api' + '/sensor' + '/'+ sensor_id ##sensors[sensor_id]
	response = requests.get(url_)
	# if response.status_code ==200:
	res = response.json()
	return res['data']


def getmodeldata(model_id,data):
	# url_ = url + '/api' + '/model' + '/' + model_id
    url_ = url + '/model' + '/' + model_id
    response = requests.post(url_ , json = data)
	# if response.status_code ==200:
    res = response.json()
    return res['result']


def getsensordata1(sensor_id):
    sensor_topic = sensors[sensor_id]
    print("Sensor_Tpic: ", sensor_topic)
    res = getkafkadata(sensor_topic)
    
    return res['data']


def getkafkadata(topic):
    consumer = KafkaConsumer(topic,bootstrap_servers=['52.140.63.83:9092'], max_partition_fetch_bytes=19048576)
    
    # print("Consumer: ",consumer)
    # stream = ""
    for message in consumer:
        print("Message Recieved: ", topic)
        try:
            res = json.loads(message.value)
            data = {
                'data':res
            }
            return data
        except:
            stream = BytesIO(message.value)
        # print("Stream:", type(stream.getvalue()))
        image = Image.open(stream).convert("RGB")
        frame = np.array(image)
        stream.close()
        # image.show()
        image = frame.tolist()
        data = {
            'data': {
                'image': image
            }
        }

        return data

def s

def setcontrollerdata(sensor_id):
    sensor_topic = sensors[sensor_id]
    print("Sensor_Tpic: ", sensor_topic)
    setkafkadata(sensor_topic)