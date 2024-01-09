# weird video bug
import cv2
import numpy as np

def cartoonize_image(img, ds_factor = 4, sketch_mode = False):
    # convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # apply median filter to the grayscale image
    img_gray = cv2.medianBlur(img_gray, 7)
    
    # detect edges in the image and threshold it
    edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize = 5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    
    # 'mask' is the sketch of the image
    if sketch_mode:
        img_sketch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        # using th 3x3 kernel to play with the thickness
        kernel = np.ones((3, 3), np.uint8)
        img_eroded = cv2.erode(img_sketch, kernel, iterations= 1)
        return cv2.cvtColor(img_eroded, 5)
    
    # resize the image to a smaller size for faster computation
    img_small = cv2.resize(img, None, fx=1.0/ds_factor, fy=1.0/ds_factor, interpolation=cv2.INTER_AREA)
    num_repetitions = 10
    sigma_color = 5
    sigma_space = 7
    size = 5
    
    # apply bilateral filter the image multiple times
    for i in range(num_repetitions):
        img_small = cv2.bilateralFilter(img_small, size, sigma_color, sigma_space)
        
        img_output = cv2.resize(img_small, None, fx=ds_factor, fy=ds_factor, interpolation= cv2.INTER_LINEAR)
        
        dst = np.zeros(img_gray.shape)
        
        # Add the thick boundary lines to the umage using 'AND' operator
        dst = cv2.bitwise_and(img_output, img_output, mask = mask)
        return dst
    
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    
    cur_char = -1
    prev_char = -1
    
    while True:
        ret, frame = cap.read()
        # a bug during resizing
        frame = cv2.resize(frame, None, fx= 0.5, fy= 0.5, interpolation= cv2.INTER_AREA)
         
        c = cv2.waitKey(1)
        if c == 27:
            break
        
        if c > -1 and c != prev_char:
            cur_char = c
        prev_char = c
        
        if cur_char == ord('s'):
            cv2.imshow("Cartoonize", cartoonize_image(frame, sketch_mode= True))
        elif cur_char == ord('c'):
            cv2.imshow("Cartoonize", cartoonize_image(frame, sketch_mode= False))
        else:
            cv2.imshow("Cartoonize", frame)
            
        cap.release()
        cv2.destroyAllWindows()
