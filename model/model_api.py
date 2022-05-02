from flask import Flask, jsonify, request
import emotion_detection
import face_detection
import motion
import os
import dotenv
# dotenv.load_dotenv() 
# PORT = os.environ.get("SERVICE_PORT")
PORT=8000
# Assuming : Model Class file is included in "dependencies"
app = Flask(__name__)


# @app.route('/get_result', methods=['POST'])
# def get_result():
#     res = request.get_json()
#     return jsonify({"result":dog_model.predict(**res)})

@app.route('/model/1', methods=['POST','GET'])
def get_result_1():
    res = request.get_json()
    return jsonify({"result":face_detection.predict(**res)})

@app.route('/model/2',  methods=['POST','GET'])
def get_result_2():
    res = request.get_json()
    return jsonify({"result":emotion_detection.predict(**res)})

@app.route('/model/3',  methods=['POST','GET'])
def get_result_3():
    res = request.get_json()
    return jsonify({"result":motion.predict(**res)})

if __name__ == "__main__":
    app.run(debug=False, port=PORT, host='0.0.0.0')