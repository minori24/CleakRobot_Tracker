# Servo Controller

import pca9685
import smbus
import time
import math

class ServoController:

    SERVO_MAX = 2400
    SERVO_MIN = 1000
    SERVO_CENTER = 1500
    SERVO_CH_X = 8
    SERVO_CH_Y = 9
    SERVO_CH_MOUTH = 3
    mag_x = 1
    mag_y = 1
    servo_x = SERVO_CENTER
    servo_y = SERVO_CENTER

    def __init__(self):
        self.driver = pca9685.PCA9685(I2CBus=1, I2CAddr=0x40, freq=47)

    def moveAbsoluteX(self, position):
        self.driver.setPulseWidth(self.SERVO_CH_X, position)
        self.servo_x = position

    def moveAbsoluteY(self, position):
        self.driver.setPulseWidth(self.SERVO_CH_Y, position)
        self.servo_y = position

    def moveAbsoluteMouth(self, position):
        self.driver.setPulseWidth(self.SERVO_CH_MOUTH, position)

    def update(self, pxDeltaX, pxDeltaY):
        # if pxDeltaX < 0 and posX < SERVO_MAX:
        #     posX = self.servo_x - pxDeltaX
        #
        # if pxDeltaX > 0 and posX > SERVO_MIN:
        #     posX = self.servo_x - pxDeltaX
        #
        # if pxDeltaY < 0 and posY < SERVO_MAX:
        #     posY = self.servo_y - pxDeltaY
        #
        # if pxDeltaY > 0 and posY > SERVO_MIN:
        #     posY = self.servo_y - pxDeltaY
        posX = self.servo_x - pxDeltaX
        posY = self.servo_y + pxDeltaY
        self.driver.setPulseWidth(self.SERVO_CH_X, posX)
        self.driver.setPulseWidth(self.SERVO_CH_Y, posY)
        self.servo_x = int(posX)
        self.servo_y = int(posY)
        print "x:" + str(self.servo_x) + " y:" + str(self.servo_y)

    def moveMouth(self, openclose):
        pass



if __name__ == '__main__':
    servo = ServoController()
    i = 1000

    servo.moveAbsoluteX(1500)
    servo.moveAbsoluteY(1500)


    # while True:
    #     if(i < 2000):
    #         servo.moveAbsoluteX(i)
    #         servo.moveAbsoluteY(i)
    #         i += 20
    #
    #     if(i >= 2000 and i < 3000):
    #         servo.moveAbsoluteX(4000 - i)
    #         servo.moveAbsoluteY(4000 - i)
    #         i += 20
    #
    #     if(i >= 3000):
    #         i = 1000
    #
    #         time.sleep(0.02)

    while True:
        x = 1500 + int(500 * math.cos(math.radians(i)))
        y = 1500 + int(500 * math.sin(math.radians(i)))
        print str(x)
        servo.moveAbsoluteX(x)
        # servo.moveAbsoluteY(y)
        if i >= 360:
            i = 0
        i += 1
        time.sleep(0.01)
    # #
    # i = 1500
    # j = 1500
    # while True:
    #     x = random.randint(1200, 1800)
    #     y = random.randint(1200, 1800)
    #
    #     while i < x:
    #         servo.moveAbsoluteX(i)
    #         i += 10
    #         time.sleep(0.05)
    #         pass
    #
    #     while i > x:
    #         servo.moveAbsoluteX(i)
    #         i -= 10
    #         time.sleep(0.05)
    #         pass
    #
    #     while j < y:
    #         servo.moveAbsoluteY(j)
    #         j += 10
    #         time.sleep(0.05)
    #         pass
    #
    #     while j > y:
    #         servo.moveAbsoluteY(j)
    #         j -= 10
    #         time.sleep(0.05)
    #         pass
