#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import sys
import curses


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
decStepper = mh.getStepper(200,1)
raStepper = mh.getStepper(200,2)
decStepper.setSpeed(20)
raStepper.setSpeed(20)

print("booting uex_controller")


while(1) :
    
    data = sys.stdin.readline()
	
    if data > "" :
		dataString = str(data)
		print "[py] got something: %r" % (dataString)
		
		if dataString == "up\n" :
			print "[py] got up"
			raStepper.step(1,Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
		elif dataString == "down\n" :
			print "[py] got down"
			raStepper.step(1,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
		elif dataString == "left\n" :
			print "[py] got left"
			decStepper.step(1,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
		elif dataString == "right\n" :
			print "[py] got right"
			decStepper.step(1,Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
			
        #myStepper2.step(20,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)



