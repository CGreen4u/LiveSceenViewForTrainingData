import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui #keep for window to stay correct size --this model did not work due to direct X so we import the below
from DirectXkeys import PressKey,ReleaseKey, W, A, S, D


def draw_lines(img, lines):
    try:
        for line in lines: #[[[2,3,5,6]]]
            coords = line[0] #we must reference the lines in the lines so we call the code below
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3) # draws line on image
    except:
        pass
#we are looking for the region of interest --what part of the image do you need to look at for information
def roi(img, vertices):
    mask = np.zeros_like(img) #create a np array that looks like our image all zeros
    cv2.fillPoly(mask, vertices, 255) # filled in at full value of 255 as in pixel
    masked = cv2.bitwise_and(img, mask)
    return masked
    


def process_image(original_image):  #simple processing of image
    #we are wanting to dumb down the image
    #here we are just converting the image to gray so its simpiler to be viewed.
    #note you cant just throw nn at things we need to have confidence in the lanes
    #in this case we are wanting to show the lanes more clearly in order to identfy them
    #alternativly we could play the game ourselves and train the game to play like we play using nivida plugin
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #canny edge detection - thresholds can be tweeked
    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    processed_image = cv2.GaussianBlur(processed_image, (5,5), 0)
    vertices = np.array([[10,500], [10,300], [300,200], [500,200], [800,300], [800,500]], np.int32)
    processed_image = roi(processed_image, [vertices])

    #hue lines              edges - you need to be sure there is edge detection feed in in our case we are using Canny
    lines = cv2.HoughLinesP(processed_image, 1, np.pi/180, 180, np.array([]), 100, 5) #just edges image passed on
    draw_lines(processed_image, lines) #this connects lines that are not connected where-on processed image, with-lines we just found
    return processed_image



#this is a simple count down script giving us time to go through game and before we start process
##for i in list(range(4))[::-1]:
##    print(i+1)
##    time.sleep(1)



def screen_record(): 
    last_time = time.time()
    while(True):
        printscreen =  np.array(ImageGrab.grab(bbox=(0,40,800,640))) # 800x600 windowed mode
        new_screen = process_image(printscreen) #calling function above
        #Movement starts here------------------
##        print('down')
##        PressKey(W) #pyautogui.keyDown('w')
##        time.sleep(3)
##        print('up')
##        ReleaseKey(W) #pyautogui.keyUp('w')
        #Movement ends above------------------
        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window', new_screen)
        #cv2.imshow('window2',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
screen_record()



