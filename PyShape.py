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
        ##A python dict to store all the shapes
        self.shapes_dict = {"triangle" : 0, "rectangle" : 0, "pentagon" : 0, "hexagon" : 0, "circle" : 0}
        
        ##Read the image
        self.image_read = cv2.imread(self.image_path)
        ##Turn it gray for thresholding
        self.gray = cv2.cvtColor(self.image_read, cv2.COLOR_BGR2GRAY)  
        ##Threshold it to get edges
        self.unusedvar, self.edit = cv2.threshold(self.gray, 220, 255, cv2.THRESH_BINARY)
        ##Get contours to identify joints in lines
        self.contours, self.unusedvar = cv2.findContours(self.edit, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    def get_all_shapes(self):       
        
        for cnt in self.contours:
            
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
            
            ###Set a minimum noise filtering area, I guess 400 is good enough
            if(area > 400) :
                if (len(approx)==3):
                    self.shapes_dict["triangle"] += 1
                elif (len(approx)==4):
                    self.shapes_dict["rectangle"] += 1
                elif (len(approx)==5):
                    self.shapes_dict["pentagon"] += 1
                elif (len(approx)==6):
                    self.shapes_dict["hexagon"] += 1
                    
        return self.shapes_dict ##returns a dictionary with the frequency of occurance of the shapes
    
    
    
    
    ###Shows the shapes with their names and indexes
    def show_shapes(self):
        
        ###text details
        font = cv2.FONT_HERSHEY_COMPLEX
        fontScale = 0.5
        color = (255,0,0)
        thickness = 1
        
        ###initialize indexes
        shape_index = {"triangle" : 0, "rectangle" : 0, "pentagon" : 0, "hexagon" : 0, "circle" : 0}
        
        for cnt in self.contours:
            
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
            
            ###Set a minimum noise filtering area, I guess 400 is good enough
            if(area > 400) :
                if (len(approx)==3):
                    cv2.drawContours(self.image_read,[approx],0,(0,255,0),5)
                    self.image_read = cv2.putText(self.image_read, 'triangle'+str(shape_index["triangle"]), (x,y), font, fontScale, color, thickness, cv2.LINE_AA) #image = cv2.putText(image, 'OpenCV', org, font,  fontScale, color, thickness, cv2.LINE_AA)
                    shape_index["triangle"] += 1
                elif (len(approx)==4):
                    cv2.drawContours(self.image_read,[approx],0,(0,0,255),5)
                    self.image_read = cv2.putText(self.image_read, 'rectangle'+str(shape_index["rectangle"]), (x,y), font, fontScale, color, thickness, cv2.LINE_AA) #image = cv2.putText(image, 'OpenCV', org, font,  fontScale, color, thickness, cv2.LINE_AA) 
                    shape_index["rectangle"] += 1
                elif (len(approx)==5):
                    cv2.drawContours(self.image_read,[approx],0,(0,255,255),5)
                    self.image_read = cv2.putText(self.image_read, 'pentagon'+str(shape_index["pentagon"]), (x,y), font, fontScale, color, thickness, cv2.LINE_AA) #image = cv2.putText(image, 'OpenCV', org, font,  fontScale, color, thickness, cv2.LINE_AA) 
                    shape_index["pentagon"] += 1
                elif (len(approx)==6):
                    cv2.drawContours(self.image_read,[approx],0,(255,0,0),5)                    
                    self.image_read = cv2.putText(self.image_read, 'hexagon'+str(shape_index["hexagon"]), (x,y), font, fontScale, color, thickness, cv2.LINE_AA) #image = cv2.putText(image, 'OpenCV', org, font,  fontScale, color, thickness, cv2.LINE_AA) 
                    shape_index["hexagon"] += 1
            ###Loop ends
                    
        cv2.imshow("Image with indexes", self.image_read)
        cv2.waitKey(0)
            
        
            
            
    ###Returns a dictionary of the coordinates of the corners of the shape with the given name and index
    def get_corners(self, name, index): 
        ##Pre-requisites for names and index detection
        flag = False
        shapes_name_to_number = {"triangle" : 3, "rectangle" : 4, "pentagon" : 5, "hexagon" : 6, "circle" : -1}
        shapes_index = {"triangle" : 0, "rectangle" : 0, "pentagon" : 0, "hexagon" : 0, "circle" : 0}
        
        for cnt in self.contours:
            
            approximate_corners = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
            ##Get starting coordinates
            x = approximate_corners.ravel()[0]
            y = approximate_corners.ravel()[1]
            area = cv2.contourArea(approximate_corners)
            
            ###Exclude the outer boundary
            if(x < 5) :
                continue
            if(y < 5) :
                continue
                       
            ###Set a minimum noise filtering area, I guess 400 is good enough
            if(area > 400) :
                if (len(approximate_corners)==shapes_name_to_number[name]):
                    if(shapes_index[name] == index):
                        flag = True
                        return approximate_corners 
                        ### A numpy array containing the coordinates of the corners
                        ### where approximate_corner[n] denotes the (n+1)th corner coordinate
                    else:
                        shapes_index[name] += 1
        if(flag == False):
            return None ###If shape and index are not found : return None
        
        
        
        
    ###Returns the area of the shape with a particular name and index
    #def get_area(name, index):
    
    ###Also implement Hough circles for detecting circles

    def close(self):
        cv2.destroyAllWindows()

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