from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import cv2
import warnings
warnings.filterwarnings("ignore")

'''
Requirements for this function to work:

The following libraries have to be installed:
-numpy
-tensorflow
-cv2

2. A Model file of the name "emotions_final.h5" has to be in the folder "above" this .py file

3. The face detection model file also has to be in the same folder as this python file.
    Download it from this link: 
    https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml

Usage Guide:
-call the function emotion_detection and give the path to the image you want to analyze 
-> the function will return a String value containing the detected emotion or probable mistake


'''

def emotion_detection(img_path):
  #load test image:
  frame = cv2.imread(img_path)

  #load the previously trained and saved model
  emotion_model = load_model("../emotions_final.h5")

  #load face classifier to aid the detection, if file does not exist, download it
  face_classifier = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

  #save the emotion labels in correct order
  emotion_label = ['Angry', "Distgust", 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']


  try:
    #catching exception caused by the image incorrectly or passing passing no image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  except Exception:
    return "picture not passed correctly"

  faces = face_classifier.detectMultiScale(gray,1.3,5)
  if str(type(faces)) == "<class 'tuple'>":
    return "no face found"

  for (x,y,w,h) in faces:
      cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
      roi_gray = gray[y:y+h,x:x+w]
      roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

      roi = img_to_array(roi_gray)
      roi = np.expand_dims(roi,axis=0)

      preds = emotion_model.predict(roi)
      label = emotion_label[np.argmax(preds[0])]
      return label