import cv

image = cv.LoadImageM(".\Images\Tornado5.png")

def foo(num):
  num = 1

cv.NamedWindow("TestOutRaw", 1)
cv.ShowImage("TestOutRaw", image)
cv.CreateTrackbar("HueHigh", "TestOutRaw", 10, 179, foo )

cv.WaitKey(0)

