#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import sys

#create motor hat
mh = Adafruit_MotorHAT()

#auto cut motors on shut down

def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

#setting up stepper1 200 steps/rev
myStepper = mh.getStepper(200,1)
myStepper2 = mh.getStepper(200,2)
myStepper.setSpeed(1000)
myStepper2.setSpeed(20)

myStepper2.step(20,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)


while(1) :
    print "reading"
    data = sys.stdin.readline();
    if data == "up/n" :
        myStepper2.step(20,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)



