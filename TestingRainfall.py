import numpy as np
import cv2
import math
image=cv2.imread("india_political.png",0)
imagelogo=cv2.imread("Logo.png")
imagelogo=cv2.resize(imagelogo,(190,95))
#The list  has been created using dataset
StateData=["Kerala","Tamil Nadu","NA","Goa","Karnatka","Andhra Pradesh",
           "Maharastra","Orrisa","NA","Chattishgarh","NA",
           "Mizoram","Tripura","West Bengal","NA",
           "Jharkhand","Gujarat","NA","Manipur","NA","NA","Meghalaya",
           "Madhya Pradesh","Nagaland","NA","NA","Bihar","Assam","Sikkim",
           "Arunachal Pradesh","Uttar Pradesh","Rajasthan","Haryana","Dehradun",
           "Punjab","Himachal Pradesh","Jammu and Kashmir"]
RainFallData=[100,150,120,132,122,143,120,88,54,34,36,122,230,123,
              110,92,96,91,90,122,120,134,154,113,82,85,81,76,73,72,73,66,28,65,
              46,34,120]
CropData=["Jowar","Gram","Gram","Jowar","Oats","Sorghum","Rye","Barley","Rye","Millet",
          "Barley","Sorghum","Rye","Maize","Barley","Buckwheat","Rice","Corn","Millet","Wheat","Rice","Quinoa","Jowar",
          "Barley","Millet","Rye","Rice","Corn","Rye","Rice","Barley","Corn","Gram","Millet","Rye","Wheat","Gram"]
resize=cv2.resize(image,(750,750))
thresh=cv2.threshold(resize,240,
                     256,cv2.THRESH_BINARY)
thresh2=cv2.threshold(resize,240,
                      256,cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh2[1],cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


img=thresh[1].copy()
cv2.drawContours(img,contours,-1,(0,0,255),cv2.FILLED)
new_image=cv2.bitwise_not(img,img)
new_image2=cv2.bitwise_and(new_image,thresh[1])

contours,_= cv2.findContours(new_image2,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
new_imagess=cv2.cvtColor(new_image2,cv2.COLOR_GRAY2BGR)
contourdetails=[]
for cnt in contours:
    x,y,w,h=cv2.boundingRect(cnt)
    contourdetails.append([x,y,x+w,y+h])
def LetTheComputerDoTheJob(co_ordinates):
    indexcount=0
    for cnt in contours:
        if (cv2.pointPolygonTest(cnt,(co_ordinates[0],co_ordinates[1]),True)>=0):
            if StateData[indexcount]!="NA":
                rendered_image=cv2.cvtColor(resize,cv2.COLOR_GRAY2BGR)
                logo=imagelogo.copy()
                city="City: "+StateData[indexcount]
                rainfall="Annual Rainfall: "+str(RainFallData[indexcount])+" cm"
                crops="Most Preferred Crop: "
                cropss=CropData[indexcount]
                cv2.putText(logo, city, (5, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), lineType=4)
                cv2.putText(logo, rainfall, (5, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), lineType=4)
                cv2.putText(logo, crops, (5, 66), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), lineType=4)
                cv2.putText(logo, cropss, (45, 84), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), lineType=4)
                cv2.drawContours(rendered_image,[cnt],0,(0,255,0),3)
                #print(StateData[indexcount])
                return(rendered_image,logo)
        indexcount=indexcount+1
rendered_image=None    
def draw_circle(event,x,y,flags,param):
    global ren
    global mouseX,mouseY
    if event == cv2.EVENT_MOUSEMOVE:
        #cv2.circle(img,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y
        try:
            rendered_image,logo=LetTheComputerDoTheJob([mouseX,mouseY])
        except Exception as e:
            pass
        try:
            cv2.imshow('image',rendered_image)
            cv2.imshow('dataWindow',logo)
        except:
            cv2.imshow('image',new_imagess)
            cv2.imshow('dataWindow',imagelogo)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
cv2.imshow("image",new_imagess)
while True:
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break
