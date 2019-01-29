#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
import wpilib.drive
#Smart dashboard import
from networktables import NetworkTables
#rev import (only necessary for CAN and low level functions like PID, otherwise, use wpilib.spark)
import rev


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        # Set up smart Dashboard
        self.sd = NetworkTables.getTable("SmartDashboard")
        # Set up motors
        self.motor = rev.CANSparkMax(11, rev.MotorType.kBrushless)
        self.encoder = rev._impl.CANEncoder(self.motor)
        self.motor_PID = rev._impl.CANPIDController(self.motor)
        # self.right_motor = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        # self.drive = wpilib.drive.DifferentialDrive(self.left_motor, self.right_motor)
        # Set up the joystick
        self.stick = wpilib.Joystick(0)
        # set up the timer
        self.timer = wpilib.Timer()
        # Set up the PID Gains as constants.  These Values are Reccommended by Rev
        self.kP = .1
        self.kI = .0001
        self.kD = 0
        self.kIz = 0
        self.kFF = 0
        self.kMaxOutput = .5
        self.kMinOutput = -.5
        self.rotations = 0.0
        self.maxRPM = 5700
        # Put the PID gains into shuffleboard
        self.sd.putNumber("P Gain", self.kP)
        self.sd.putNumber("I Gain", self.kI)
        self.sd.putNumber("D Gain", self.kD)
        self.sd.putNumber("I Zone", self.kIz)
        self.sd.putNumber("Feed Forward", self.kFF)
        self.sd.putNumber("Max Output", self.kMaxOutput)
        self.sd.putNumber("Min Output", self.kMinOutput)
        self.sd.putNumber("Setpoint", self.rotations)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            self.motor.set(.5)  # Drive forwards at half speed (just to test the motor)
        else:
            self.motor.set(0)  # Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        # Get the trimmed PID gains from Shuffleboard
        p = self.sd.getNumber("P Gain", 0)
        i = self.sd.getNumber("I Gain", 0)
        d = self.sd.getNumber("D Gain", 0)
        iz = self.sd.getNumber("I Zone", 0)
        ff = self.sd.getNumber("Feed Forward", 0)
        max = self.sd.getNumber("Max Output", 0)
        min = self.sd.getNumber("Min Output", 0)
        rotations = self.sd.getNumber("Setpoint", 0)
        
        # implement the gains from shuffleboard

        self.motor_PID.setP(p)
        self.motor_PID.setI(i)
        self.motor_PID.setD(d)
        self.motor_PID.setIZone(iz)
        self.motor_PID.setFF(ff)
        self.motor_PID.setOutputRange(min, max)

        # Post the gains Back to shuffleboard.
        self.sd.putNumber("Current P Gain", p)
        self.sd.putNumber("Current I Gain", i)
        self.sd.putNumber("Current D Gain", d)
        self.sd.putNumber("Current I Zone", iz)
        self.sd.putNumber("Current Feed Forward", ff)
        self.sd.putNumber("Current Max Output", max)
        self.sd.putNumber("Current Min Output", min)

        # Get the setpoint from the joystick    
        setPoint = rotations

        #Tell the motor to zoom to the setpoint
        self.motor_PID.setReference(rotations, rev.ControlType.kPosition)

        # Push setpoint and actual rotations to shuffleboard
        self.sd.putNumber("Your Chosen SetPoint", rotations)
        self.sd.putNumber("Current Value", self.encoder.getPosition())



if __name__ == "__main__":

    # Run the program
    wpilib.run(MyRobot)
