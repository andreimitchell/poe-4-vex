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

# PID control algorithm
def pid(target, actual, prevError, integral, Kp, Ki, Kd, deltaTime):
    # Calculate error
    error = target - actual

    # Calculate integral and derivative
    newIntegral = integral + error * deltaTime
    derivative = (error - prevError) / deltaTime

    # Return output
    return error, newIntegral, Kp * error + Ki * newIntegral + Kd * derivative

def driveStraight(distance, normalVelocity, reverse=False):
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

    prevTime = brain.timer.time(SECONDS)
    prevAngleRight = 0
    prevAngleLeft = 0
    prevErrorRight = 0
    prevErrorLeft = 0
    integralRight = 0
    integralLeft = 0

    spinMotors(direction * normalVelocity, direction * normalVelocity)
    wait(10, MSEC)

    # while loop will run until right encoder value = total count value
    while ((rightMotor.position(DEGREES) < count) ^ reverse):
        encoderValues()  # Print encoder values

        deltaTime = brain.timer.time(SECONDS) - prevTime
        prevTime = brain.timer.time(SECONDS)
        prevAngleRight = rightMotor.position(DEGREES)
        prevAngleLeft = leftMotor.position(DEGREES)
        actualSpeedRight = (rightMotor.position(DEGREES) - prevAngleRight) / deltaTime
        actualSpeedLeft = (leftMotor.position(DEGREES) - prevAngleLeft) / deltaTime

        # Compute motor speeds and correct as necessary
        if (abs(rightMotor.position(DEGREES)) < abs(leftMotor.position(DEGREES))): # left faster
            prevErrorLeft, integralLeft, deltaVelocityLeft = pid(actualSpeedRight, actualSpeedLeft, prevErrorLeft, integralLeft, 0.1, 0, 0.1, deltaTime)
            spinMotors(direction * normalVelocity, direction * (normalVelocity + deltaVelocityLeft))
        elif (abs(rightMotor.position(DEGREES)) > abs(leftMotor.position(DEGREES))): # right faster
            prevErrorRight, integralRight, deltaVelocityRight = pid(actualSpeedLeft, actualSpeedRight, prevErrorRight, integralRight, 0.1, 0, 0.1, deltaTime)
            spinMotors(direction * (normalVelocity + deltaVelocityRight), direction * normalVelocity)
        else: # both equal
            spinMotors(direction * normalVelocity, direction * normalVelocity)
        time.sleep(0.01)
    
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
    normalVelocity = 50            # Desired velocity
    slowVelocity = 44              # Velocity to slow down to

    # Define turn velocity
    turnVelocity = 40

    # Constants
    halfWidth = 5.5
    wheelDiameter = 4
    angle = 90
    multiplier = 1.08
    encoderAngle = multiplier * halfWidth * angle * 2 / wheelDiameter

    while True:
        brain.screen.set_cursor(1, 1)   # Move cursor to row 1, column 1

        bump()                          # Wait for bump switch to be pressed

        wait(0.5, SECONDS)            # Wait so robot is not affected by hand

        # Time the running motors
        brain.timer.clear()

        for i in range(4):
            # Drive forward (distance in inches)
            driveStraight(44, normalVelocity)

            wait(0.5, SECONDS)

            # Point turn left
            pointTurn(encoderAngle, normalVelocity, 1)

            wait(0.5, SECONDS)

main()  # Run main function