#!/usr/bin/env python
import io
import cv2
import picamera
import numpy as np
import numpy
import time

# Camera Controller
class Eye:
	def __init__(self):
		self.camera = 1

	def get_figure_cg(self):
                yellow_lower_h = 10
                yellow_lower_s = 90
                yellow_lower_v = 140
                
                yellow_upper_h = 60
                yellow_upper_s = 255
                yellow_upper_v = 255

		stream = io.BytesIO()
		with picamera.PiCamera() as camera:
			camera.resolution = (320,240)
			camera.framerate=32
			camera.capture(stream,format='jpeg')
			
                # allow the camera to warmup
                time.sleep(0.5)
                
		buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
		image = cv2.imdecode(buff,1)
		
                #flip the image first vertically then horizontically
                image = cv2.flip(image,0)
                image = cv2.flip(image,1)

                cv2.imwrite('test11.jpg',image)

                #Convert to HSV
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                cv2.imwrite('hsv.jpg',hsv)
                blurred = cv2.GaussianBlur(hsv,(5,5),0)
                cv2.imwrite('blurred.jpg',blurred)
              
                #find all the 'yellow' shapes in the image
                upper = np.array([yellow_upper_h, yellow_upper_s, yellow_upper_v], dtype=np.uint8)
                lower = np.array([yellow_lower_h,yellow_lower_s,yellow_lower_v], dtype=np.uint8)

                #threshold to only get yellow
                masked = cv2.inRange(blurred, lower, upper)
                cv2.imwrite('masked.jpg',masked)

                contours, hierarchy = cv2.findContours(masked,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		for cnt in contours:
		    approx = cv2.approxPolyDP(cnt,0.035*cv2.arcLength(cnt,True),True)
		    if len(approx)==3:
                        print 'Triangle Shape is detected ..'
		        M = cv2.moments(cnt)
		        cx = int(M['m10']/M['m00'])
		        cy = int(M['m01']/M['m00'])
		        print 'Centroid(x,y): ' +'('+str(cx)+','+str(cy)+')'
		        
			if str(cx)=='nan':
				cx = -5
			if str(cy)=='nan':
				cy = -5
			if cx ==None:
				cx=-5
			if cy==None:
				cy=-5
			
			self.centroid = [cx, cy]
		        return self.centroid
		    else:
		    	self.centroid = [-5, -5]
		    	print 'Return: '
		    	print self.centroid
		    	return self.centroid
