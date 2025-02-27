import time
from turtle import left
import cv2 as cv
import numpy as np
import pyautogui as pg

"""
Пример отработки входа в приложение
"""

def click(img, h, ros=None , shir = None):
    board = pg.locateOnScreen(f'{img}' , confidence=h)
    
    if shir:
        pg.click(board.left + ros , board.top + shir)
        time.sleep(1)
    
    elif ros:
        pg.click(board.left + ros , board.top + board.height/2)
        time.sleep(1)
    else:
        if board:
            pg.click(board.left + board.width/2 , board.top + board.height/2)
            time.sleep(1)

click('skrins/point.png', 0.7) 
click('skrins/search.png', 0.7, 70)
click('skrins/search.png', 0.7, 70)
