# -*- coding: utf-8 -*-
import pygame
import time
import os
import PIL.Image

from threading import Thread
from pygame.locals import *
from time import sleep
from PIL import Image, ImageDraw

import sys

reload(sys)
sys.setdefaultencoding('utf8')

# initialise global variables
Numeral = ""  # Numeral is the number display
Message = ""  # Message is a fullscreen message
BackgroundColor = ""
CountDownPhoto = ""
CountPhotoOnCart = ""
SmallMessage = ""  # SmallMessage is a lower banner message
TotalImageCount = 0  # Counter for Display and to monitor paper usage
PhotosPerCart = 30  # Selphy takes 16 sheets per tray
imagecounter = 0
imagefolder = 'Photos'
templatePath = os.path.join('Photos', 'Template', "template.png")  # Path of template image
ImageShowed = False
Printing = False
BUTTON_PIN = 25
# IMAGE_WIDTH = 558
# IMAGE_HEIGHT = 374
IMAGE_WIDTH = 550
IMAGE_HEIGHT = 360

# Load the background template
bgimage = PIL.Image.open(templatePath)

# initialise pygame
pygame.init()  # Initialise pygame

infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)  # Full screen
background = pygame.Surface(screen.get_size())  # Create the background object
background = background.convert()  # Convert it to a background

screenPicture = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)  # Full screen
backgroundPicture = pygame.Surface(screenPicture.get_size())  # Create the background object
backgroundPicture = background.convert()  # Convert it to a background

transform_x = infoObject.current_w  # how wide to scale the jpg when replaying
transfrom_y = infoObject.current_h  # how high to scale the jpg when replaying


# camera.framerate             = 24
# camera.sharpness             = 0
# camera.contrast              = 8
# camera.saturation            = 0
# camera.ISO                   = 0
# camera.video_stabilization   = False
# camera.exposure_compensation = 0
# camera.exposure_mode         = 'auto'
# camera.meter_mode            = 'average'
# camera.awb_mode              = 'auto'
# camera.image_effect          = 'none'
# camera.color_effects         = None
# camera.crop                  = (0.0, 0.0, 1.0, 1.0)


# A function to handle keyboard/mouse/device input events
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()


# set variables to properly display the image on screen at right ratio
def set_demensions(img_w, img_h):
    # Note this only works when in booting in desktop mode.
    # When running in terminal, the size is not correct (it displays small). Why?

    # connect to global vars
    global transform_y, transform_x, offset_y, offset_x

    # based on output screen resolution, calculate how to display
    ratio_h = (infoObject.current_w * img_h) / img_w

    if (ratio_h < infoObject.current_h):
        # Use horizontal black bars
        # print "horizontal black bars"
        transform_y = ratio_h
        transform_x = infoObject.current_w
        offset_y = (infoObject.current_h - ratio_h) / 2
        offset_x = 0
    elif (ratio_h > infoObject.current_h):
        # Use vertical black bars
        # print "vertical black bars"
        transform_x = (infoObject.current_h * img_w) / img_h
        transform_y = infoObject.current_h
        offset_x = (infoObject.current_w - transform_x) / 2
        offset_y = 0
    else:
        # No need for black bars as photo ratio equals screen ratio
        # print "no black bars"
        transform_x = infoObject.current_w
        transform_y = infoObject.current_h
        offset_y = offset_x = 0

def DisplayText(fontSize, textToDisplay):
    global Numeral
    global Message
    global screen
    global background
    global pygame
    global ImageShowed
    global screenPicture
    global backgroundPicture
    global CountDownPhoto

    if (BackgroundColor != ""):
        # print(BackgroundColor)
        background.fill(pygame.Color("black"))
    if (textToDisplay != ""):
        # print(displaytext)
        font = pygame.font.Font("seguisym.ttf", fontSize)
        text = font.render(textToDisplay, True, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        if (ImageShowed):
            backgroundPicture.blit(text, textpos)
        else:
            background.blit(text, textpos)


def UpdateDisplay():
    # init global variables from main thread
    global Numeral
    global Message
    global screen
    global background
    global pygame
    global ImageShowed
    global screenPicture
    global backgroundPicture
    global CountDownPhoto

    background.fill(pygame.Color("white"))  # White background
    # DisplayText(100, Message)
    # DisplayText(800, Numeral)
    # DisplayText(500, CountDownPhoto)

    if (BackgroundColor != ""):
        # print(BackgroundColor)
        background.fill(pygame.Color("black"))
    if (Message != ""):
        # print(displaytext)
        font = pygame.font.Font("seguisym.ttf", 100)
        text = font.render(str(Message).encode('utf-8'), True, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        if (ImageShowed):
            backgroundPicture.blit(text, textpos)
        else:
            background.blit(text, textpos)

    if (Numeral != ""):
        # print(displaytext)
        font = pygame.font.Font("seguisym.ttf", 800)
        text = font.render(str(Numeral).encode('utf-8'), True, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        if (ImageShowed):
            backgroundPicture.blit(text, textpos)
        else:
            background.blit(text, textpos)

    if (CountDownPhoto != ""):
        # print(displaytext)
        font = pygame.font.Font("seguisym.ttf", 500)
        text = font.render(str(CountDownPhoto).encode('utf-8'), True, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        if (ImageShowed):
            backgroundPicture.blit(text, textpos)
        else:
            background.blit(text, textpos)

    if (ImageShowed == True):
        screenPicture.blit(backgroundPicture, (0, 0))
    else:
        screen.blit(background, (0, 0))

    pygame.display.flip()
    return


def ShowPicture(file, delay):
    global pygame
    global screenPicture
    global backgroundPicture
    global ImageShowed
    backgroundPicture.fill((0, 0, 0))
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, screenPicture.get_size())  # Make the image full screen
    # backgroundPicture.set_alpha(200)
    backgroundPicture.blit(img, (0, 0))
    screen.blit(backgroundPicture, (0, 0))
    pygame.display.flip()  # update the display
    ImageShowed = True
    time.sleep(delay)


# display one image on screen
def show_image(image_path):
    screen.fill(pygame.Color("white"))  # clear the screen
    img = pygame.image.load(image_path)  # load the image
    img = img.convert()
    set_demensions(img.get_width(), img.get_height())  # set pixel dimensions based on image
    x = (infoObject.current_w / 2) - (img.get_width() / 2)
    y = (infoObject.current_h / 2) - (img.get_height() / 2)
    screen.blit(img, (x, y))
    pygame.display.flip()

def WaitForEvent():
    global pygame
    NotEvent = True
    while NotEvent:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_DOWN:
                    NotEvent = False
                    return
        time.sleep(0.2)

def main(threadName, *args):
    while True:
        show_image('images/start_camera.png')
        DisplayText(50, "Pózoljatok")
        WaitForEvent()
        time.sleep(0.2)


# launch the main thread
Thread(target=main, args=('Main', 1)).start()
