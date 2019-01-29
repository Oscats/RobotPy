#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        #Drivetrain
        self.left_motor = wpilib.Spark(0)
        self.right_motor = wpilib.Spark(1)
        self.drive = wpilib.drive.DifferentialDrive(self.left_motor, self.right_motor)
        #joystick
        self.stick = wpilib.Joystick(1)
        self.timer = wpilib.Timer()
        #solenoids
        self.pinion = wpilib.DoubleSolenoid(0,1)
        self.doubleSolenoid = wpilib.DoubleSolenoid(2,3)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
        else:
            self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        #DriveTrain
        self.drive.arcadeDrive(self.stick.getY(), self.stick.getX())
        
        #Pneumatics
        if (self.stick.getRawButton(2) == (1)):
            self.pinion.set(1)
        elif (self.stick.getRawButton(3)):
            self.pinion.set(2)
        else:
             self.pinion.set(0)
        if (self.stick.getRawButton(4) == (1)):
            self.doubleSolenoid.set(1)
        elif (self.stick.getRawButton(1)):
            self.doubleSolenoid.set(2)
        else:
             self.doubleSolenoid.set(0)

if __name__ == "__main__":
    wpilib.run(MyRobot)
