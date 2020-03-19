# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:58:43 2020

@author: Richeek Das
"""

import numpy as np
import cv2

class PyShape :
    
    image_path = None
    
    def __init__(self, image_path) :
        self.image_path = image_path
    
    def get_all_shapes(self):
        ##A python dict to store all the shapes
        shapes_dict = {"triangle" : 0, "rectangle" : 0, "pentagon" : 0, "hexagon" : 0, "circle" : 0}
        
        ##Read the image
        image_read = cv2.imread(self.image_path)
        ##Turn it gray for thresholding
        gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)  
        ##Threshold it to get edges
        _, edit = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
        ##Get contours to identify joints in lines
        contours, _ = cv2.findContours(edit, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
        for cnt in contours:
            
            approx = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
            ##Get starting coordinates
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            area = cv2.contourArea(approx)
            
            ###Exclude the outer boundary
            if(x < 5) :
                continue
            if(y < 5) :
                continue
            ###
            
            ###Set a minimumnoise filtering area, I guess 400 is good enough
            if(area > 400) :
                if (len(approx)==3):
                    shapes_dict["triangle"] += 1
                elif (len(approx)==4):
                    shapes_dict["rectangle"] += 1
                elif (len(approx)==5):
                    shapes_dict["pentagon"] += 1
                elif (len(approx)==6):
                    shapes_dict["hexagon"] += 1
                    
        return shapes_dict ##returns a dictionary with the frequency of occurance of the shapes
    
    ###Shows the shapes with their names and indexes
    #def show_shapes():
        
    ###Returns a dictionary of the coordinates of the corners of the shape with the given name and index
    #def get_corners(name, index): 

    ###Returns the area of the shape with a particular name and index
    #def get_area(name, index):
    
    ###Also implement Hough circles for detecting circles



"""
if(area > 400) :
    print(len(approx))
    if (len(approx)==5):
        print("pentagon")
        cv2.drawContours(img,[approx],0,255,5)
    elif (len(approx)==3):
        print("triangle")
        cv2.drawContours(img,[approx],0,(0,255,0),5)
    elif (len(approx)==4):
        print("rectangle")
        cv2.drawContours(img,[approx],0,(0,0,255),5)
        



cv2.imshow('imag', img)
cv2.imshow('mask', edit)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""