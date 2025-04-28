# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Alex Oh, Alp Tanyel                                          #
# 	Created:      4/28/2025, 10:02:29 AM                                       #
# 	Description:  A1 Wait States                                               #
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
def spinMotors(vel):

    # Set motor velocities
    rightMotor.set_velocity(vel, PERCENT)
    leftMotor.set_velocity(vel, PERCENT)

    # Spin motors
    rightMotor.spin(FORWARD)
    leftMotor.spin(FORWARD)

    # Time the running motors
    brain.timer.clear()
    brain.screen.print("Timer Started")

# Stop motors
def stopMotors():
    rightMotor.stop()
    leftMotor.stop()

def main():

    # Set stopping mode for motors
    rightMotor.set_stopping(BRAKE)
    leftMotor.set_stopping(BRAKE)

    motorVelocity = 50  # Velocity in # (vmax = 200 rpm)
    brain.screen.set_cursor(1, 1)

    bump()  # Wait for bump switch to be pressed

    spinMotors(motorVelocity)   # Spin motors forward
    wait(1000, MSEC)  # Wait time (timer) value in milliseconds
    stopMotors()  # Stop motors

    brain.screen.set_cursor(2, 1)   # Move cursor down one row
    brain.screen.print(f"Time: {brain.timer.time(SECONDS)}")  # Print timer value in seconds