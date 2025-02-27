# import pytesseract
# import cv2 as cv

# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# img = cv.imread('trede5.png')
# # img = cv.Canny(img,100,200)

# config = r'--oem 3 --psm 6'
# print(pytesseract.image_to_string(img,config=config,lang='eng'))

import easyocr
from win_Capture import WindowCapture

wincap = WindowCapture('Albion Online Launcher')

screenshot = wincap.get_screenshot()

render = easyocr.Reader(['en'])
print(render.readtext(screenshot))