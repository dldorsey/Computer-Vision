# Track objects in webcam based on Hue value. 
# Use object position to control cursor on macbook
# Optimised to track yellow beak of rubber duck!
# ctrl+c  Quits program
# robbierickman.blogspot.com


import cv
import sys 
from pylab import *
from objc import loadBundle, loadBundleFunctions  #required for mouse position.



# Set mouse position in OSX
class ETMouse():    
    def setMousePosition(self, x, y):
        bndl = loadBundle('CoreGraphics', globals(), 
                '/System/Library/Frameworks/ApplicationServices.framework')
        loadBundleFunctions(bndl, globals(), 
                [('CGWarpMouseCursorPosition', 'v{CGPoint=dd}')])
        CGWarpMouseCursorPosition((x, y))


#    Convert image to HSV and threshold to produced binary image based on Hue value.
def thresholdImage(img):
    #allocate temp image based on size of input img
    img_hsv = cv.CreateImage((img.width,img.height),8,3)   #3 channel
    img_thresh = cv.CreateImage((img.width,img.height),8,1)#1 channel

    cv.CvtColor(img, img_hsv, cv.CV_BGR2HSV)    
    cv.InRangeS(img_hsv, cv.Scalar(5, 100, 100), cv.Scalar(30, 255, 255), img_thresh);
    
    return(img_thresh)
    
#    Plot a histogram showing Hue vs Saturation.  Not necessary for function of program, useful for optimising image thresholds
#    Samples from box in top corner of camera image only.
def histogram(src):
    # Set ccd sampling region.
    cv.SetImageROI(src,(10,10,100,100))
    
    # Convert to HSV
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)

    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
    s_plane = cv.CreateMat(cv.GetSize(src)[1], cv.GetSize(src)[0], cv.CV_8UC1)
    h_plane = cv.CreateMat(cv.GetSize(src)[1], cv.GetSize(src)[0], cv.CV_8UC1)
    


    cv.Split(hsv, h_plane, s_plane, None, None)
    planes = [h_plane, s_plane]

    h_bins = 28
    s_bins = 5
    hist_size = [h_bins, s_bins]
    # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
    h_ranges = [0, 180]
    # saturation varies from 0 (black-gray-white) to
    # 255 (pure spectrum color)
    s_ranges = [0, 255]
    ranges = [h_ranges, s_ranges]
    scale = 15
    
    
    # calculate histogram
    hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)
    cv.CalcHist([cv.GetImage(i) for i in planes], hist)
    (_, max_value, _, _) = cv.GetMinMaxHistValue(hist)
    
    # Reset cv sampling region to full CCD Area
    cv.ResetImageROI(src)


    # plot histogram data
    hist_img = cv.CreateImage((h_bins*scale, s_bins*scale), 8, 3)

    for h in range(h_bins):
        for s in range(s_bins):
            bin_val = cv.QueryHistValue_2D(hist, h, s)
            intensity = cv.Round(bin_val * 255 / max_value)
            cv.Rectangle(hist_img,(h*scale, s*scale),((h+1)*scale - 1, (s+1)*scale - 1),cv.RGB(intensity, intensity, intensity),cv.CV_FILLED)
    return hist_img

    

    


    
#    Filter noisy pixels using custom kernel size. 
#    Removes visually insignificant noise such as speckles
def erodeImage(img):
    kernel = cv.CreateStructuringElementEx(9,9,5,5, cv.CV_SHAPE_CROSS) 
    # Erode- replaces pixel value with lowest value pixel in kernel
    cv.Erode(img,img,kernel,2)
    # Dilate- replaces pixel value with highest value pixel in kernel
    cv.Dilate(img,img,kernel,2)
    return img
    
def contour_iterator(contour):
                while contour:
                        yield contour
                        contour = contour.h_next()
                        
    
def findImageContour(img,frame):
    storage = cv.CreateMemStorage()
    cont = cv.FindContours(img, storage,cv.CV_RETR_EXTERNAL,cv.CV_CHAIN_APPROX_NONE,(0, 0))
    max_center = [None,0]
    for c in contour_iterator(cont):
    # Number of points must be more than or equal to 6 for cv.FitEllipse2
    # Use to set minimum size of object to be tracked.
        if len(c) >= 60:
            # Copy the contour into an array of (x,y)s
            PointArray2D32f = cv.CreateMat(1, len(c), cv.CV_32FC2)
            for (i, (x, y)) in enumerate(c):
                PointArray2D32f[0, i] = (x, y)
                # Fits ellipse to current contour.
                (center, size, angle) = cv.FitEllipse2(PointArray2D32f)
                # Only consider location of biggest contour  -- adapt for multiple object tracking
            if size > max_center[1]:
                max_center[0] = center
                max_center[1] = size
                angle = angle
                        
            if True:
                # Draw the current contour in gray
                gray = cv.CV_RGB(255, 255, 255)
                cv.DrawContours(img, c, gray, gray,0,1,8,(0,0))
                        
    if max_center[1] > 0:
        # Convert ellipse data from float to integer representation.
        center = (cv.Round(max_center[0][0]), cv.Round(max_center[0][1]))
        size = (cv.Round(max_center[1][0] * 0.5), cv.Round(max_center[1][1] * 0.5))
        color = cv.CV_RGB(255,0,0)
        
        cv.Ellipse(frame, center, size,angle, 0, 360,color, 3, cv.CV_AA, 0)
        ETMouse().setMousePosition(2.6*max_center[0][0]-150, 2*max_center[0][1]-100)
    



def main():
    # create windows for use later
    cv.NamedWindow("LaserDuckOut",1)
    cv.NamedWindow("Theshold_IMG",1)
    cv.NamedWindow("HSV Histogram",1)
    # initiate camera
    capture = cv.CreateCameraCapture(0)
    
    # grab frame from camera
    if capture:
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
                
            cv.Flip(frame, frame,1)
            
            hist = histogram(frame)

            img = thresholdImage(frame)
            img = erodeImage(img)

            findImageContour(img,frame)
            
            
            # Mark out sampling region for histogram
            cv.Rectangle(frame,(10,10),(110,110),(0,255,0),1,0)


            # outputs image to windows created previously
            cv.ShowImage("Threshold_IMG",img)
            cv.ShowImage("LaserDuckOut",frame)
            cv.ShowImage("HSV_Histogram",hist)
                        
            if cv.WaitKey(10) >= 0:
                break
                
    cv.DestroyWindow("LaserDuckOut")
    cv.DestroyWindow("Threshold_IMG")
    cv.DestroyWindow("HSV_Histogram")
            







if __name__=='__main__':
    main()