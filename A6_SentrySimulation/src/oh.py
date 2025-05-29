# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Alex Oh, Alp Tanyel, Andrei Mitchell                         #
# 	Created:      5/21/2025                                                    #
# 	Description:  A6 Sentry Simulation                                         #
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

# Print encoder values to screen
def encoderValues():
    brain.screen.set_cursor(1, 1)                       # Set cursor 
    brain.screen.print("Right Encoder: ")
    brain.screen.print(rightMotor.position(DEGREES))    # Print right encoder
    brain.screen.set_cursor(1, 25)
    brain.screen.print("Left Encoder: ")
    brain.screen.print(leftMotor.position(DEGREES))     # Print left encoder

def driveStraight(distance, normalVelocity, slowVelocity, reverse=False):
    direction = 1
    if reverse:
        direction = -1

    diameter = 4    # 4" diameter wheel
    circumference = math.pi * diameter

    # Calculate the count value required
    count = (distance / circumference) * 360

    # Reset the encoders
    leftMotor.set_position(0, DEGREES)
    rightMotor.set_position(0, DEGREES)

    normalVel = 5
    slowVel = 0

    # while loop will run until right encoder value = total count value
    while ((rightMotor.position(DEGREES) < count) ^ reverse):
        encoderValues()  # Print encoder values

        # Compute motor speeds and correct as necessary
        if (rightMotor.position(DEGREES) == leftMotor.position(DEGREES)): # both equal
            spinMotors(direction * normalVel, direction * normalVel)
        elif ((rightMotor.position(DEGREES) < leftMotor.position(DEGREES)) ^ reverse): # left faster
            # spinMotors(rightMotorVelocity, leftMotorVelocity)
            spinMotors(direction * normalVel, direction * slowVel)
        else: # right faster
            spinMotors(direction * slowVel, direction * normalVel)
        
        normalVel += 0.1
        slowVel += 0.1
        if normalVel > normalVelocity:
            normalVel = normalVelocity
        if slowVel > slowVelocity:
            slowVel = slowVelocity
    
    stopMotors()

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

    # Define normal and slow velocities
    normalVelocity = 45            # Desired velocity
    slowVelocity = 40              # Velocity to slow down to

    # Define turn velocity
    turnVelocity = 40

    # Constants
    halfWidth = 5.5
    wheelDiameter = 4
    angle = 90
    multiplier = 1.097
    encoderAngle = multiplier * halfWidth * angle * 2 / wheelDiameter

    while True:
        brain.screen.set_cursor(1, 1)   # Move cursor to row 1, column 1

        bump()                          # Wait for bump switch to be pressed

        wait(0.3, SECONDS)            # Wait so robot is not affected by hand

        # Clear brain
        brain.timer.clear()

        # Drive forward (distance in inches)
        driveStraight(45, normalVelocity, slowVelocity)

        wait(0.5, SECONDS)

        # Point turn left
        pointTurn(encoderAngle - 2, normalVelocity, 1)

        wait(0.5, SECONDS)

        # Drive forward (distance in inches)
        driveStraight(45, normalVelocity, slowVelocity)

        wait(0.5, SECONDS)

        # Point turn left
        pointTurn(encoderAngle, normalVelocity, 1)

        wait(0.5, SECONDS)

        # Drive forward (distance in inches)
        driveStraight(45, normalVelocity, slowVelocity)

        wait(0.5, SECONDS)

        # Point turn left
        pointTurn(encoderAngle, normalVelocity, 1)

        wait(0.5, SECONDS)

        # Drive forward (distance in inches)
        driveStraight(45, normalVelocity, slowVelocity)

        wait(0.5, SECONDS)

        # Point turn left
        pointTurn(encoderAngle, normalVelocity, 1)

        wait(0.5, SECONDS)

main()  # Run main function 