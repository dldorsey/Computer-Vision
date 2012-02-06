import cv

cv.NamedWindow("TestOutRaw", 1)
cv.NamedWindow("TestOutFiltered", 1)
capture = cv.CreateCameraCapture(0)

struct = cv.CreateStructuringElementEx(10,10,0,0,cv.CV_SHAPE_RECT)

def thresholdImage(img):
    #allocate temp image based on size of input img
    img_hsv = cv.CreateImage((img.width,img.height),8,3)   #3 channel
    img_thresh = cv.CreateImage((img.width,img.height),8,1)#1 channel

    cv.CvtColor(img, img_hsv, cv.CV_BGR2HSV)    
    cv.InRangeS(img_hsv, cv.Scalar(155, 50, 50), cv.Scalar(175, 255, 255), img_thresh)
    
    return(img_thresh)
    
def erodeImage(img):
    kernel = cv.CreateStructuringElementEx(9,9,5,5, cv.CV_SHAPE_CROSS) 
    # Erode- replaces pixel value with lowest value pixel in kernel
    cv.Erode(img,img,struct,2)
    # Dilate- replaces pixel value with highest value pixel in kernel
    cv.Dilate(img,img,struct,2)
    return img

if capture:
  while True:
    frame = cv.QueryFrame(capture)
    if not frame:
        cv.WaitKey(0)
        break
    cv.ShowImage("TestOutRaw", frame)
    
    #img = thresholdImage(frame)
    img = erodeImage(frame)
    img = thresholdImage(img)
    cv.ShowImage("TestOutFiltered", img)
    
    if cv.WaitKey(1) >= 0:
      break