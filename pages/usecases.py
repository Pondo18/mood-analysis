import tempfile
import random
import string

import cv2


class AnalyseRecordedVideo:
    def __init__(self, blob_video):
        self.blob_video = blob_video
        self.filename = ""
        self.frame_distance = 0

    def execute(self):
        file = tempfile.NamedTemporaryFile(suffix='webm')
        with file as f_vid:
            f_vid.write(self.blob_video.read())
            self.filename = f_vid.name
            self.frame_distance = self._get_frame_distance()
            self._create_frames_as_jpg()

    def _get_frame_distance(self):
        cap = cv2.VideoCapture(self.filename)
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
        cap = cv2.VideoCapture(self.filename)
        count = 0
        frame_base_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:
                if count % self.frame_distance == 0:
                    print('Read %d frame: ' % count, ret)
                    cv2.imwrite(f"{frame_base_name}_{count}.jpg", frame)  # save frame as JPEG file
                count += 1
            else:
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

