# Servo Controller

import pca9685
import smbus
import time
import math

class Robot:
    SERVO_MAX = 2400
    SERVO_MIN = 1000

    def __init__(self, name, chX, chY, chMouth):
        self.name = name
        self.chX = chX
        self.chY = chY
        self.chMouse = chMouth
        self.offsetX = 0
        self.offsetY = 0
        self.posX = 1500
        self.posY = 1500

    def setOffset(self, offsetX, offsetY):
        self.offsetX = offsetX
        self.offsetY = offsetY

class ServoController:

    SERVO_MAX = 2400
    SERVO_MIN = 1000
    SERVO_CENTER = 1500


    def __init__(self):
        self.driver = pca9685.PCA9685(I2CBus=1, I2CAddr=0x40, freq=47)
        self.robots = []

    def addRobot(self, name, offsetX, offsetY):
        robot = Robot(name="0", chX=8, chY=9, chMouse=0)
        self.robots.append(robot)

    def moveAbsoluteX(self, name, position):
        for robot in self.robots:
            print robot.posX
            if robot.name == name:
                self.driver.setPulseWidth(robot.chX, position)
                robot.posX = position

    def moveAbsoluteY(self, name, position):
        for robot in self.robots:
            if robot.name == name:
                self.driver.setPulseWidth(robot.chY, position)
                robot.posY = position

    def moveAbsoluteMouth(self, position):
        self.driver.setPulseWidth(self.SERVO_CH_MOUTH, position)

    def updateAll(self, pxDeltaX, pxDeltaY):
        for robot in self.robots:

            posX = robot.posX + (pxDeltaX + robot.offsetX)
            posY = robot.posY - (pxDeltaY + robot.offsetY)
            # print posX
            if posX <= self.SERVO_MAX and posX >= self.SERVO_MIN:
                self.driver.setPulseWidth(robot.chX, posX)
                robot.posX = posX


            if posY <= self.SERVO_MAX and posY >= self.SERVO_MIN:
                self.driver.setPulseWidth(robot.chY, posY)
                robot.posY = posY

    def moveMouth(self, openclose):
        pass

if __name__ == '__main__':
    servo = ServoController()
    i = 1000

    servo.addRobot("1", 0, 0)
    servo.moveAbsoluteX("1", 1500)
    servo.moveAbsoluteY("1", 1500)
    x = 0
    y = 0
    while True:
        _x = int(500 * math.cos(math.radians(i)))
        _y = int(500 * math.sin(math.radians(i)))
        # print str(_x)
        servo.updateAll(_x - x, _y - y)
        x = _x
        y = _y

        if i >= 360:
            i = 0
        i += 1
        time.sleep(0.01)
