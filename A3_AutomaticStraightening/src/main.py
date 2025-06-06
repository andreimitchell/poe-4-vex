# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Alex Oh, Alp Tanyel                                          #
# 	Created:      5/12/2025                                                    #
# 	Description:  A1 Driving Straight                                          #
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

    # while loop will run until right encoder value = total count value
    while ((rightMotor.position(DEGREES) < count) ^ reverse):
        encoderValues()  # Print encoder values

        # Compute motor speeds and correct as necessary
        if (rightMotor.position(DEGREES) == leftMotor.position(DEGREES)): # both equal
            spinMotors(direction * normalVelocity, direction * normalVelocity)
        elif ((rightMotor.position(DEGREES) < leftMotor.position(DEGREES)) ^ reverse): # left faster
            # spinMotors(rightMotorVelocity, leftMotorVelocity)
            spinMotors(direction * normalVelocity, direction * slowVelocity)
        else: # right faster
            spinMotors(direction * slowVelocity, direction * normalVelocity)
    
    stopMotors()

def main():
    # Set stopping mode for motors
    rightMotor.set_stopping(BRAKE)
    leftMotor.set_stopping(BRAKE)

    # Define normal and slow velocities
    normalVelocity = 60            # Desired velocity
    slowVelocity = 54              # Velocity to slow down to

    while True:
        brain.screen.set_cursor(1, 1)   # Move cursor to row 1, column 1

        bump()                          # Wait for bump switch to be pressed

        # Time the running motors
        brain.timer.clear()
        brain.screen.print("Timer Started")

        # Drive forward (distance in inches)
        driveStraight(120, normalVelocity, slowVelocity)

        brain.screen.set_cursor(2, 1)   # Move cursor down one row
        brain.screen.print("Time: " + str(brain.timer.time(SECONDS)))    # Print timer value in seconds

        # wait(1, SECONDS)

        # Drive reverse
        # driveStraight(120, normalVelocity, slowVelocity, True)

main()  # Run main function