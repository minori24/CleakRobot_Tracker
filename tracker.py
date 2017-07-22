import cv2
import numpy as np
import servo
import time
import threading

class Tracker:

    face_cascade_path = '/home/minori/opencv/opencv_itseez/opencv-3.2.0/data/haarcascades/haarcascade_frontalface_default.xml'
    eye_cascade_path = '/home/minori/opencv/opencv/data/haarcascade_eye.xml'
    smile_cascade_path = '/home/minori/opencv/opencv/data/haarcascade_smile.xml'

    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
    smile_cascade = cv2.CascadeClassifier(smile_cascade_path)
    
    def __init__(self):
        self.srv = servo.ServoController()
        self.trackerThread = threading.Thread(target=self.track, name="tracker")
        self.trackingState = False
        self.trackerThread.setDaemon(True)
        self.event_stopTracking = threading.Event()
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    def startTracking(self):
        self.trackingState = True
        self.event_stopTracking.clear()
        self.trackerThread.start()

        print "start tracking"

    def stopTracking(self):
        self.trackingState = False
        self.event_stopTracking.set()

    def track(self):

        while not self.event_stopTracking.is_set():
            if self.capture.isOpened:
                _, frame = self.capture.read()
                height, width = frame.shape[:2]
                center_x = width / 2
                center_y = height / 2
                rects = self.trackFace(frame)

                if len(rects) > 0:
                    # pick one largest rect
                    rect = max(rects, key=(lambda x: x[2] * x[3]))

                    x = rect[0]
                    y = rect[1]
                    w = rect[2]
                    h = rect[3]

                    dx = (x + w / 2) - center_x
                    dy = (y + h / 2) - center_y
                    self.srv.update(dx * 0.1, dy * 0.1)
                else:
                    print "no objects found"
                    # self.srv.moveAbsoluteX(1500)
                    # self.srv.moveAbsoluteY(1900)

        self.capture.release()

    def trackFace(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=1, minSize=(1, 1))
        print faces
        return faces
        #
        # for (x, y, w, h) in faces:
        #     #cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #     roi_gray = gray[y:y+h, x:x+w]
        #     roi_color = img[y:y+h, x:x+w]

            # eyes = eye_cascade.detectMultiScale(roi_gray)
            #
            # for (ex, ey, ew, eh) in eyes:
            #     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            #
            # smile = smile_cascade.detectMultiScale(roi_gray,
            #                                        scaleFactor=1.7,
            #                                        minNeighbors=22,
            #                                        minSize=(25, 25),
            #                                        )
            #
            # for (ex, ey, ew, eh) in smile:
            #     cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)
            #
    def trackRed(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        mask = np.zeros(h.shape, dtype=np.uint8)
        mask[((h < 20) | (h > 200)) & (s > 128)] = 255
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []

        for contour in contours:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            rects.append(np.array(rect))
        return rects

    def getCurrentPosition(self):
        pass

    def getTrackingState(self):
        return self.trackingState

if __name__ == "__main__":

    tracker = Tracker()
    tracker.startTracking()
    while True:
        i = raw_input()
        if i == "c":
            tracker.stopTracking()
            break
