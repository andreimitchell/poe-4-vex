# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Alex Oh, Alp Tanyel, Andrei Mitchell                         #
# 	Created:      5/29/2025                                                    #
# 	Description:  A8 Transport Challenge                                       #
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

    normalVel = 8
    slowVel = 0
    increment = 1

    # while loop will run until right encoder value = total count value
    while abs(rightMotor.position(DEGREES)) < count:
        # Compute motor speeds and correct as necessary
        if (abs(rightMotor.position(DEGREES)) < abs(leftMotor.position(DEGREES))): # left faster
            spinMotors(direction * normalVel, direction * slowVel)
        elif (abs(rightMotor.position(DEGREES)) > abs(leftMotor.position(DEGREES))): # right faster
            spinMotors(direction * slowVel, direction * normalVel)
        else: # both equal
            spinMotors(direction * normalVel, direction * normalVel)
        
        normalVel += increment
        slowVel += increment
        if normalVel > normalVelocity:
            normalVel = normalVelocity
        if slowVel > slowVelocity:
            slowVel = slowVelocity
        
        wait(10, MSEC)
    
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

# Function to control lift arm rotation
def liftArm(motorVelocity, angle):
    # Reset the lift arm rotation sensor
    liftArmRotation.reset_position()
    liftMotor.set_velocity(motorVelocity, PERCENT)

    brain.screen.set_cursor(1, 1)  # Move cursor to row 1, column 1
    brain.screen.print("Initial Rotation: " + str(liftArmRotation.position(DEGREES)))

    # Rotate the lift arm depending on the decimal angle (positive or negative)
    if angle > 0:
        while liftArmRotation.position(DEGREES) < angle:
            liftMotor.spin(FORWARD)
        liftMotor.stop()
        wait(0.5, SECONDS)
    else:
        while liftArmRotation.position(DEGREES) > angle:
            liftMotor.spin(REVERSE)
        liftMotor.stop()
        wait(0.5, SECONDS)
    
    brain.screen.set_cursor(2, 1)  # Move cursor to row 2, column 1
    brain.screen.print("Final Rotation: " + str(liftArmRotation.position(DEGREES)))

def calculateEncoderAngle(angle, multiplier):
    """
    Calculate the encoder angle for a point turn based on the angle,
    half width of the robot, and wheel diameter.
    """
    halfWidth = 5.5  # Half width of the robot in inches
    wheelDiameter = 4  # Diameter of the wheels in inches

    return multiplier * halfWidth * angle * 2 / wheelDiameter

def main():
    # Set stopping mode for motors
    rightMotor.set_stopping(BRAKE)
    leftMotor.set_stopping(BRAKE)
    liftMotor.set_stopping(HOLD)

    # Define motor velocities
    normalVelocity = 50 # Desired drivetrain velocity
    slowVelocity = 42   # Velocity to slow down to
    turnVelocity = 40   # Velocity for point turns
    liftVelocity = 30   # Velocity for lift arm

    while True:
        bump()                          # Wait for bump switch to be pressed

        wait(0.3, SECONDS)            # Wait so robot is not affected by hand

        # Drive forward (distance in inches)
        driveStraight(73, normalVelocity, slowVelocity)
        wait(0.5, SECONDS)
        liftArm(liftVelocity, 50)  # Rotate lift arm up 45 degrees
        wait(0.5, SECONDS)
        driveStraight(12, normalVelocity, slowVelocity, reverse=True)  # Drive backward
        wait(0.5, SECONDS)
        pointTurn(calculateEncoderAngle(90, 1.1), turnVelocity, -1)  # Point turn right
        wait(0.5, SECONDS)
        driveStraight(64, normalVelocity, slowVelocity)
        wait(0.5, SECONDS)
        pointTurn(calculateEncoderAngle(34, 1.1), turnVelocity, 1)    # Point turn left
        wait(0.5, SECONDS)
        driveStraight(16, normalVelocity, slowVelocity)
        wait(0.5, SECONDS)
        liftArm(liftVelocity, -50)  # Rotate lift arm down 45 degrees
        wait(0.5, SECONDS)
        liftArm(liftVelocity, 50)  # Rotate lift arm up 45 degrees
        wait(0.5, SECONDS)
        driveStraight(3, normalVelocity, slowVelocity, reverse=True)  # Drive backward
        wait(0.5, SECONDS)
        pointTurn(calculateEncoderAngle(90, 1.1), turnVelocity, -1)   # Point turn right
        wait(0.5, SECONDS)
        driveStraight(18, normalVelocity, slowVelocity, reverse=True)
        wait(0.5, SECONDS)
        pointTurn(calculateEncoderAngle(56, 1.1), turnVelocity, 1)    # Point turn left
        wait(0.5, SECONDS)
        driveStraight(42, normalVelocity, slowVelocity, reverse=True)

main()  # Run main function