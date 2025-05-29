# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Alex Oh, Alp Tanyel                                          #
# 	Created:      5/14/2025                                                    #
# 	Description:  A4 Point Turn                                          #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
        
# Robot configuration code
rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
liftMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
inertial_1 = Inertial(Ports.PORT5)
liftArmRotation = Rotation(Ports.PORT6, False)
bumpSwitch = Bumper(brain.three_wire_port.a)

# Bump switch function: will hold program until switch is pressed
def bump():
    while(not bumpSwitch.pressing()):
        wait(10, MSEC)
        pass

# Spin motors
def spinMotors(vel1, vel2):

    # Set motor velocities
    rightMotor.set_velocity(vel1, PERCENT)
    leftMotor.set_velocity(vel2, PERCENT)

    # Spin motors
    rightMotor.spin(FORWARD)
    leftMotor.spin(FORWARD)

# Stop motors
def stopMotors():
    rightMotor.stop()
    leftMotor.stop()

# Define left point turn (direction = 1) and right point turn (direction = -1)
def pointTurn(turnCount, motorVelocity, direction):
    # Reset the encoders
    leftMotor.set_position(0, DEGREES)
    rightMotor.set_position(0, DEGREES)

    # while loop will run until right encoder value = total count value
    while (abs(rightMotor.position(DEGREES)) < turnCount):
        spinMotors(direction * motorVelocity, -direction * motorVelocity)
    
    stopMotors()

def main():
    # Set stopping mode for motors
    rightMotor.set_stopping(BRAKE)
    leftMotor.set_stopping(BRAKE)

    # Define turn velocity
    turnVelocity = 70

    # Constants
    halfWidth = 5.5
    wheelDiameter = 4
    angle = 90
    encoderAngle = halfWidth * angle * 2 / wheelDiameter

    while True:
        bump()  # Wait for bump switch to be pressed

        pointTurn(570, turnVelocity, 1)  # Left point turn
        # wait(1, SECONDS)  # Wait for 1 second
        # pointTurn(40, turnVelocity, -1)  # Right point turn

main()  # Run main function