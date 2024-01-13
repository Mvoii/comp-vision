import sys

import cv2
import numpy as np

# draw rectangle on top of the input image
def draw_rectangle(event, x, y, flags, param):
    global x_init, y_init, drawing, top_left_pt, bottom_right_pt, img_orig
    
    # detect mouse click
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_init, y_init = x, y
        
    # detecting mouse movement
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            top_left_pt, bottom_right_pt = (x_init, y_init), (x, y)
            img[y_init:y, x_init:x] = 255 - img_orig[y_init:y, x_init:x]
            cv2.rectangle(img, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
    
    # detecting mouse button up event
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        top_left_pt, bottom_right_pt = (x_init, y_init), (x, y)
        
        # create the "negative" film effect for the selected region
        img[y_init:y, x_init:x] = 255 - img[y_init:y, x_init:x]
        
        # draw rectangle around selected region
        
if __name__ == "__main__":
    img_input = cv2.imread(sys.argv[1])
    
    drawing = False
    img = np.copy(img_input)
