import cv2
import numpy as np

class PyShape :

    def __init__(self, image_path) :
        self.PI = 3.14159265
        self.image_path = image_path
        ##A python dict to store all the shapes
        self.shapes_dict = {"triangle" : 0, "rectangle" : 0, "pentagon" : 0, "hexagon" : 0, "circle" : 0}
        ##Read the image
        self.image_read = cv2.imread(self.image_path)
        self.image_show = self.image_read.copy()
        ##Turn it gray for thresholding
        self.gray = cv2.cvtColor(self.image_show, cv2.COLOR_BGR2GRAY)
        ##Threshold it to get edges
        self.unusedvar, self.edit = cv2.threshold(self.gray, 220, 255, cv2.THRESH_BINARY)
        ##Get contours to identify joints in lines
        self.contours, self.unusedvar = cv2.findContours(self.edit, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.gray_blurred = cv2.blur(self.gray, (3, 3))
        # Apply Hough transform on the blurred image.
        self.detected_circles = cv2.HoughCircles(self.gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 60, minRadius = 0, maxRadius = 0)

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
        ###Loop ends
        # Draw circles that are detected.
        if self.detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles_np = np.uint16(np.around(self.detected_circles))

            for pt in detected_circles_np[0, :]:
                _, _, r = pt[0], pt[1], pt[2]
                if(r >= 11) :
                    self.shapes_dict["circle"] += 1
        ###Circles found

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
                    cv2.drawContours(self.image_show,[approx],0,(0,255,0),2)
                    self.image_show = cv2.putText(self.image_show, 'triangle'+str(shape_index["triangle"]), (x,y), font, fontScale, color, thickness, cv2.LINE_AA) #image = cv2.putText(image, 'OpenCV', org, font,  fontScale, color, thickness, cv2.LINE_AA)
                    shape_index["triangle"] += 1
                elif (len(approx)==4):
                    cv2.drawContours(self.image_show,[approx],0,(0,0,255),2)
                    self.image_show = cv2.putText(self.image_show, 'rectangle'+str(shape_index["rectangle"]), (x,y-15), font, fontScale, color, thickness, cv2.LINE_AA) #image = cv2.putText(image, 'OpenCV', org, font,  fontScale, color, thickness, cv2.LINE_AA)
                    shape_index["rectangle"] += 1
                elif (len(approx)==5):
                    cv2.drawContours(self.image_show,[approx],0,(0,255,255),2)
                    self.image_show = cv2.putText(self.image_show, 'pentagon'+str(shape_index["pentagon"]), (x,y), font, fontScale, color, thickness, cv2.LINE_AA) #image = cv2.putText(image, 'OpenCV', org, font,  fontScale, color, thickness, cv2.LINE_AA)
                    shape_index["pentagon"] += 1
                elif (len(approx)==6):
                    cv2.drawContours(self.image_show,[approx],0,(255,0,0),2)
                    self.image_show = cv2.putText(self.image_show, 'hexagon'+str(shape_index["hexagon"]), (x,y), font, fontScale, color, thickness, cv2.LINE_AA) #image = cv2.putText(image, 'OpenCV', org, font,  fontScale, color, thickness, cv2.LINE_AA)
                    shape_index["hexagon"] += 1
            ###Loop ends


        # Draw circles that are detected.
        if self.detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles_np = np.uint16(np.around(self.detected_circles))

            for pt in detected_circles_np[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                if(r < 11) :
                    continue
                # Draw the circumference of the circle.
                cv2.circle(self.image_show, (a, b), r, (0, 255, 0), 2)
                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(self.image_show, (a, b), 1, (0, 0, 255), 3)
                # Put the circle name and index
                self.image_show = cv2.putText(self.image_show, "circle"+str(shape_index["circle"]) , (a+10,b+10), font, fontScale, color, thickness, cv2.LINE_AA)
                shape_index["circle"] += 1

        cv2.imshow("Image with indexes", self.image_show)
        cv2.waitKey(0)




    ###Returns a dictionary of the coordinates of the corners of the shape with the given name and index
    def get_corners(self, name, index):
        ##Pre-requisites for names and index detection
        flag = False
        shapes_name_to_number = {"triangle" : 3, "rectangle" : 4, "pentagon" : 5, "hexagon" : 6, "circle" : -1}
        shapes_index = {"triangle" : 0, "rectangle" : 0, "pentagon" : 0, "hexagon" : 0, "circle" : 0}

         # Draw circles that are detected.
        if(name == "circle"):

            if self.detected_circles is not None:

                # Convert the circle parameters a, b and r to integers.
                detected_circles_np = np.uint16(np.around(self.detected_circles))

                for pt in detected_circles_np[0, :]:
                    a, b, r = pt[0], pt[1], pt[2]
                    if(r > 11) :
                        if(shapes_index[name] == index):
                            flag = True
                            return ([a, b, r])
                        else:
                            shapes_index[name] += 1
        else :

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
            ###Loop ends


        if(flag == False):
            return None ###If shape and index are not found : return None




    ###Returns the area of the shape with a particular name and index
    def get_area(self, name, index):
        ##Pre-requisites for names and index detection
        flag = False
        shapes_name_to_number = {"triangle" : 3, "rectangle" : 4, "pentagon" : 5, "hexagon" : 6, "circle" : -1}
        shapes_index = {"triangle" : 0, "rectangle" : 0, "pentagon" : 0, "hexagon" : 0, "circle" : 0}

         # Draw circles that are detected.
        if(name == "circle"):

            if self.detected_circles is not None:

                # Convert the circle parameters a, b and r to integers.
                detected_circles_np = np.uint16(np.around(self.detected_circles))

                for pt in detected_circles_np[0, :]:
                    a, b, r = pt[0], pt[1], pt[2]
                    if(r > 11) :
                        if(shapes_index[name] == index):
                            flag = True
                            return (self.PI*r*r)
                            ### Returns the area of the shape(identified by name and index) in pixel^2
                        else:
                            shapes_index[name] += 1
        else :

            for cnt in self.contours:

                approximate_corners = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
                ##Get starting coordinates
                x = approximate_corners.ravel()[0]
                y = approximate_corners.ravel()[1]
                area_of_shape = cv2.contourArea(approximate_corners)

                ###Exclude the outer boundary
                if(x < 5) :
                    continue
                if(y < 5) :
                    continue

                ###Set a minimum noise filtering area, I guess 400 is good enough
                if(area_of_shape > 400) :
                    if (len(approximate_corners)==shapes_name_to_number[name]):
                        if(shapes_index[name] == index):
                            flag = True
                            return area_of_shape
                            ### Returns the area of the shape(identified by name and index) in pixel^2
                        else:
                            shapes_index[name] += 1

        if(flag == False):
            return -1 ###If shape and index are not found : return -1



    ###Also implement Hough circles for detecting circles
    def close(self):
        cv2.destroyAllWindows()
