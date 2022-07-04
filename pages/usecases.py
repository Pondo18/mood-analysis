import os
import tempfile
import random
import string
from base64 import b64encode

import cv2

import numpy as np


from PIL import Image

from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing.image import img_to_array

from statistics import mode


class AnalyseRecordedVideo:
    def __init__(self, blob_video):
        self.blob_video = blob_video
        self.video_path = ""
        self.frame_distance = 0
        self.image_names = []

    def execute(self):
        file = tempfile.NamedTemporaryFile(suffix='webm')
        with file as f_vid:
            f_vid.write(self.blob_video.read())
            self.video_path = f_vid.name
            self.frame_distance = self._get_frame_distance()
            self._create_frames_as_jpg()
            emotion_detection = EmotionDetection(self.image_names)
            frames, emotions = emotion_detection.execute()
            self._remove_images()
            return frames, 'No face found' if len(frames) == 0 else mode(emotions)

    def _get_frame_distance(self):
        cap = cv2.VideoCapture(self.video_path)
        frames = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frames = frames + 1
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        return int(frames / 5)

    def _create_frames_as_jpg(self):
        cap = cv2.VideoCapture(self.video_path)
        count = 0
        frame_base_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if count % self.frame_distance == 0:
                    print('Read %d frame: ' % count, ret)
                    file_name = f"{frame_base_name}_{count}.jpg"
                    self.image_names.append(file_name)
                    cv2.imwrite(file_name, frame)
                count += 1
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    def _remove_images(self):
        for image in self.image_names:
            os.remove(image)


class AnalyseImage:
    def __init__(self, image_to_analyse):
        self.image_to_analyse = image_to_analyse

    def execute(self):
        file = tempfile.NamedTemporaryFile(suffix='.jpg')
        with file as f_vid:
            f_vid.write(self.image_to_analyse.read())
            emotion_detection = EmotionDetection([f_vid.name])
            frame, _ = emotion_detection.execute()
            return frame, 'No face found' if len(frame) == 0 else frame[0].emotion


class EmotionDetection:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.emotion_model = load_model("./models/emotions_final.h5")
        self.face_classifier = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
        self.emotion_label = ['Angry', "Distgust", 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    def execute(self):
        frames = []
        emotions = []
        for image_path in self.image_paths:
            frame = np.array(Image.open(image_path))
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            except Exception as e:
                print(e)
                print("Picture could not be read", image_path)
                continue
            faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
            if str(type(faces)) == "<class 'tuple'>":
                print("no face found", image_path)
                continue
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                roi = img_to_array(roi_gray)
                roi = np.expand_dims(roi, axis=0)

                preds = self.emotion_model.predict(roi)
                label = self.emotion_label[np.argmax(preds[0])]
                emotions.append(label)
                with open(image_path, "rb") as image_file:
                    image_data = b64encode(image_file.read()).decode('utf-8')
                    frames.append(Frame(image_data, label))
                break
        return frames, emotions


class Frame:
    def __init__(self, image, emotion):
        self.image = image
        self.emotion = emotion
