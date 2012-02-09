import cv

image = cv.LoadImageM(".\Images\Tornado1.png")

def thresholdImage(img, low, high):
    #allocate temp image based on size of input img
    img_hsv = cv.CreateImage((img.width,img.height),8,3)   #3 channel
    img_thresh = cv.CreateImage((img.width,img.height),8,1)#1 channel
    
    print low, high
    
    cv.CvtColor(img, img_hsv, cv.CV_BGR2HSV)
    cv.InRangeS(img_hsv, cv.Scalar(low[0], low[1], low[2]), cv.Scalar(high[0], high[1], high[2]), img_thresh)
    
    return(img_thresh)
    
def filterImage(num):
  low_values, high_values = getTrackerValues()
  filter_image = thresholdImage(image, low_values, high_values)
  cv.ShowImage("TestOutFiltered", filter_image)

def getTrackerValues():
  low = cv.GetTrackbarPos("Low_Hue", "TestOutRaw"), cv.GetTrackbarPos("Low_Sat", "TestOutRaw"), cv.GetTrackbarPos("Low_Val", "TestOutRaw")
  high = cv.GetTrackbarPos("High_Hue", "TestOutRaw"), cv.GetTrackbarPos("High_Sat", "TestOutRaw"), cv.GetTrackbarPos("High_Val", "TestOutRaw")
  return low, high

def setupUI():  
  cv.NamedWindow("TestOutRaw", 1)
  cv.ShowImage("TestOutRaw", image)
  cv.NamedWindow("TestOutFiltered", 1)
  cv.CreateTrackbar("Low_Hue", "TestOutRaw", 0, 180, filterImage)
  cv.CreateTrackbar("Low_Sat", "TestOutRaw", 45, 255, filterImage)
  cv.CreateTrackbar("Low_Val", "TestOutRaw", 45, 255, filterImage)
  cv.CreateTrackbar("High_Hue", "TestOutRaw", 25, 180, filterImage)
  cv.CreateTrackbar("High_Sat", "TestOutRaw", 255, 255, filterImage)
  cv.CreateTrackbar("High_Val", "TestOutRaw", 255, 255, filterImage)

setupUI()  
filterImage(None)

cv.WaitKey(0)
