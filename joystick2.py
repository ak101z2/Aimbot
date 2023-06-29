import sys
import pygame
from pygame.locals import *
import serial
import time

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    # data = arduino.readline()
    # return data

def map_range(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

val = 0
while True:
    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN or event.type == JOYBUTTONUP:
            val = 0
        if event.type == JOYAXISMOTION:
            val = joystick.get_axis(0)

        val = int(map_range(val, -1, 1, 0, 255))
        if val < 0 or val > 255: val = 0
        print(val)
        write(val)