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
sensors['4'] = 'cam_4'

url = "http://127.0.0.1:8000"


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
            return res
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


