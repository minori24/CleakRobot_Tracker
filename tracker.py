import cv2
import numpy as np
import servo
import time
import threading

class Tracker:

    # distance to target, frame size at target distance
    TARGET_DISTANCE = 1.0
    FRAME_HEIGHT = 0.55
    FRAME_WIDTH = 0.9
    FRAME_X_FACTOR = 1
    FRAME_Y_FACTOR = 1

    def __init__(self):
        self.srv = servo.ServoController()
        self.trackerThread = threading.Thread(target=self.track, name="tracker")
        self.isTracking = False
        self.trackerThread.setDaemon(True)
        self.event_stopTracking = threading.Event()
        self.event_Locked = threading.Event()
        self.capture = cv2.VideoCapture(0)

    def addRobot(self):
        self.srv.addRobot(name="0", offsetX=0, offsetY=0)

    def startTracking(self):
        self.isTracking = True
        self.event_stopTracking.clear()
        self.trackerThread.start()
        self.event_Locked.clear()

        print "start tracking"

    def stopTracking(self):
        self.isTracking = False
        self.event_stopTracking.set()

    def track(self):

        while not self.event_stopTracking.is_set():
            if self.capture.isOpened:
                _, frame = self.capture.read()
                height, width = frame.shape[:2]
                center_x = width / 2
                center_y = height / 2
                rects = self.trackRed(frame)

                if len(rects) > 0:
                    # pick one largest rect
                    rect = max(rects, key=(lambda x: x[2] * x[3]))
                    self.event_Locked.set()

                    x = rect[0]
                    y = rect[1]
                    w = rect[2]
                    h = rect[3]

                    targetX = (x + w / 2) - center_x
                    targetY = center_y - (y + h / 2)

                    # print "x:" + str(1500 + targetX * self.FRAME_X_FACTOR) + " y:" + str(targetY)
                    self.srv.moveAbsoluteX("0", 1500 - targetX * self.FRAME_X_FACTOR)
                    self.srv.moveAbsoluteY("0", 1600 - targetY * self.FRAME_Y_FACTOR)

                else:
                    self.event_Locked.clear()
                    self.srv.moveAbsoluteX("0", 1500)
                    self.srv.moveAbsoluteY("0", 1600)

        self.capture.release()

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
        if event_Locked.is_set():
            return True
        else:
            return False

if __name__ == "__main__":

    tracker = Tracker()
    tracker.addRobot()
    tracker.startTracking()
    while True:
        print "wait"
        i = raw_input()
        if i == "c":
            tracker.stopTracking()
            break
