
import sys
import servo
import tracker
import random
import time

class StateMachine(object):
    def __init__(self, functions, initial_state):
        self._current_state = ''
        self._next_state = initial_state
        self._state_frame_count = 0
        self._state_func_table = functions

    def update(self):
        if self._next_state:
            self._callStateFunc('on_exit')
            self._current_state = self._next_state
            self._next_state = ''
            self._state_frame_count = 0
            self._callStateFunc('on_enter')
        self._callStateFunc('on_update')
        self._state_frame_count += 1

    def _callStateFunc(self, name):
        if self._current_state not in self._state_func_table:
            return
        functions = self._state_func_table[self._current_state]
        if name not in functions:
            return
        functions[name](self)

    def changeState(self, next_state):
        self._next_state = next_state

    def getState(self):
        return self._current_state

    def getFrameCount(self):
        return self._state_frame_count

class Animator(StateMachine):
    tracker = tracker.Tracker()
    srv = servo.ServoController()

    def __init__(self):
        self.targetX = 1500
        self.targetY = 1500
        self.currentX = 1500
        self.currentY = 1500
        self.deltaX = 0
        self.deltaY = 0
        self.count = 0
        self.duration = 20
        self.servoFactor = 20
        self.srv.moveAbsoluteX(1500)
        self.srv.moveAbsoluteY(1500)
        super(Animator, self).__init__(
            {
                'track':{
                    'on_enter':Animator._track_enter,
                    'on_update':Animator._track_update,
                    'on_exit':Animator._track_exit
                },

                'talk':{
                    'on_enter':Animator._talk_enter,
                    'on_update':Animator._talk_update,
                    'on_exit':Animator._talk_exit
                },
            },
            'track'
        )

        print("init")

    def _track_enter(self):
        print("start tracking")
        self.tracker.startTracking()

    def _track_update(self):

        if self.count >= self.duration:
            self.count = 0
            self.targetX = random.randint(1300, 2400)
            self.targetY = random.randint(1300, 2400)
            self.deltaX = (self.targetX - self.srv.servo_x) / self.duration
            self.deltaY = (self.targetY - self.srv.servo_y) / self.duration

            print("current target: " + str(self.targetX) + " " + str(self.targetY))
        else:
            self.srv.update(self.deltaX, self.deltaY)

        self.count += 1

        if self.tracker.locked:
            self.tracker.stopTracking()
            self.srv.moveAbsoluteX(self.tracker.faceX * self.servoFactor)
            self.srv.moveAbsoluteY(self.tracker.faceY * self.servoFactor)
            self.changeState('talk')
        else:
            print("searching...")

    def _track_exit(self):
        pass

    def _talk_enter(self):
        pass

    def _talk_update(self):
        print("blah blah blah")
        time.sleep(3)
        self.changeState('track')

    def _talk_exit(self):
        pass

if __name__ == "__main__":
    animator = Animator()
    while True:
        animator.update()
        time.sleep(0.1)

    print("exit")
