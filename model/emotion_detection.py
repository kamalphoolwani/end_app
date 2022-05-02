from deepface import DeepFace
import numpy as np
from pkg_resources import empty_provider
positive_emotions = ['happy', 'neutral']
negative_emotions = ['angry', 'disgust', 'fear', 'surprise', 'sad']

def predict(image):
    image = np.array(image, dtype=np.uint8)
    try:
        analyze = None
        analyze = DeepFace.analyze(image,actions=['emotion'])
    except Exception as e:
        print(e)
    if analyze is None:
        return -1
    emotion = analyze['dominant_emotion']
    emotion = emotion.lower()
    print("emotion: ", emotion)
    if emotion in positive_emotions:
        return 1
    return 0