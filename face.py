import cv2
import os
import pickle

cap = cv2.VideoCapture(0)
#  0 for the built-in webcam and 1 for the external camera
cap.set(3,640)
cap.set(4,480)

bgimage=cv2.imread("images/frame.png")



# Importing the mode images into a list
folderModePath = 'images/modes'
modePathinList = os.listdir(folderModePath)
# print(modePathinList)

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
print("Encode File Loaded")

imgModeList = []
for path in modePathinList:
    imagepath=os.path.join(folderModePath, path)
    imgModeList.append(cv2.imread(imagepath))

    #os.path.join is for to join path it will a / in between its better to use for platform indenpetne
# print(len(imgModeList))


while True:
    success,img=cap.read() # success is boolean img is numpyarry with imag etails like height weight frames channels 
    # (height, width, 3) shape is jpg image for imread returs same

    bgimage[162:162+480,55:55+640]=img
    bgimage[44:44+578,808:808+362]=imgModeList[0]
    # #cv2.imshow("hello",img) 
    cv2.imshow("bg",bgimage)
    if cv2.waitKey(1)  & 0xFF == ord('q'):
      break# Wait for a key press (any key) and then close the window


cap.release()
cv2.destroyAllWindows() # Close all OpenCV windows



