import cv

image = cv.LoadImageM(".\Images\Tornado5.png")

def thresholdImage(img,num):
    #allocate temp image based on size of input img
    img_hsv = cv.CreateImage((img.width,img.height),8,3)   #3 channel
    img_thresh = cv.CreateImage((img.width,img.height),8,1)#1 channel

    cv.CvtColor(img, img_hsv, cv.CV_BGR2HSV)    
    cv.InRangeS(img_hsv, cv.Scalar(0, 50, 50), cv.Scalar(num, 255, 255), img_thresh)
    
    return(img_thresh)
    
def filterImage(num):
  filter_image = thresholdImage(image,num)
  cv.ShowImage("TestOutFiltered", filter_image)

  
cv.NamedWindow("TestOutRaw", 1)
cv.ShowImage("TestOutRaw", image)
cv.NamedWindow("TestOutFiltered", 1)
cv.CreateTrackbar("HueHigh", "TestOutRaw", 10, 179, filterImage)

cv.WaitKey(0)

#filterImage()