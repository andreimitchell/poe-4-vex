# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Alex Oh, Alp Tanyel                                          #
# 	Created:      5/28/2025                                                    #
# 	Description:  A7 Rotation Sensor                                           #
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

# Function to control lift arm rotation
def liftArm(motorVelocity, angle):
    # Reset the lift arm rotation sensor
    liftArmRotation.reset_position()
    liftMotor.set_velocity(motorVelocity, PERCENT)

    brain.screen.set_cursor(1, 1)  # Move cursor to row 1, column 1
    brain.screen.print("Initial Rotation: " + str(liftArmRotation.position(DEGREES)))

    # Rotate the lift arm depending on the decimal angle (positive or negative)
    if angle < 0:
        while(liftArmRotation.position(DEGREES) < angle):
            liftMotor.spin(FORWARD)
        liftMotor.stop()
        wait(0.5, SECONDS)
    else:
        while(liftArmRotation.position(DEGREES) > angle):
            liftMotor.spin(REVERSE)
        liftMotor.stop()
        wait(0.5, SECONDS)
    
    brain.screen.set_cursor(2, 1)  # Move cursor to row 2, column 1
    brain.screen.print("Final Rotation: " + str(liftArmRotation.position(DEGREES)))

def main():
    # Set stopping mode for motors
    rightMotor.set_stopping(BRAKE)
    leftMotor.set_stopping(BRAKE)
    liftMotor.set_stopping(HOLD)

    # Define motor velocities
    normalVelocity = 50 # Desired drivetrain velocity
    slowVelocity = 44   # Velocity to slow down to
    turnVelocity = 40   # Velocity for point turns
    liftVelocity = 50   # Velocity for lift arm

    # Turn angle for point turn
    angle = 90

    # Constants
    halfWidth = 5.5
    wheelDiameter = 4

    # Calculate encoder angle for point turn
    multiplier = 1.097
    encoderAngle = multiplier * halfWidth * angle * 2 / wheelDiameter

    while True:
        bump()                          # Wait for bump switch to be pressed

        wait(0.3, SECONDS)            # Wait so robot is not affected by hand

        # Drive forward (distance in inches)
        driveStraight(74, normalVelocity, slowVelocity)
        wait(0.5, SECONDS)
        liftArm(liftVelocity, 45)  # Rotate lift arm up 45 degrees
        wait(0.5, SECONDS)
        driveStraight(45, normalVelocity, slowVelocity, reverse=True)  # Drive backward
        wait(0.5, SECONDS)
        pointTurn(encoderAngle, turnVelocity, -1)  # Point turn right
        liftArm(liftVelocity, -45)  # Rotate lift arm down 45 degrees

main()  # Run main function 