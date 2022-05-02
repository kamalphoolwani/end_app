from flask import Flask, jsonify, request
# import emotion_detection
import face_detection
# import motion
import os
import dotenv
dotenv.load_dotenv() 
PORT = os.environ.get("SERVICE_PORT")
# PORT=8000
# Assuming : Model Class file is included in "dependencies"
app = Flask(__name__)

@app.route('/model/1', methods=['POST','GET'])
def get_result_1():
    res = request.get_json()
    return jsonify({"result":face_detection.predict(**res)})


if __name__ == "__main__":
    app.run(debug=False, port=PORT, host='0.0.0.0')