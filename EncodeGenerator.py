import cv2
import face_recognition
import pickle
import os



# Importing the student images into a list
pathtofloder = 'images/faces'
PathinList = os.listdir(pathtofloder)
print(PathinList)

listofimages = []
uniqueids=[]
for path in PathinList:
    imagepath=os.path.join(pathtofloder, path)
    listofimages.append(cv2.imread(imagepath))
    # print(path)
    # path
    nameunique_id =os.path.splitext(path)[0]
    # print(nameunique_id)
    name, unique_id = nameunique_id.split(',')
    uniqueids.append(unique_id)
    print(uniqueids)

    # print(len(lisofimages))



def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(listofimages)
encodeListKnownWithIds = [encodeListKnown, uniqueids]
print(encodeListKnownWithIds)
print("Encoding Complete")


#pickleing the file 
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

