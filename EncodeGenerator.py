import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://facerecognition-f2f3c-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognition-f2f3c.appspot.com"  # gs://  -remove-  facerecognition-f2f3c.appspot.com

})



# Importing the student images into a list
pathtofloder = 'images/faces'
PathinList = os.listdir(pathtofloder)
print(PathinList)

listofimages = []
uniqueids=[]
names=[]
for path in PathinList:
    imagepath=os.path.join(pathtofloder, path)
    listofimages.append(cv2.imread(imagepath))
    # print(path)
    # path
    nameunique_id =os.path.splitext(path)[0]
    # print(nameunique_id)
    name, unique_id = nameunique_id.split(',')
    uniqueids.append(unique_id)
    names.append(name)
    # print(names)
    # print(uniqueids)

    # print(len(lisofimages))


###AddDatatoDatabase while importing the pics we can also uploaing  in ata base

    fileName = f'{pathtofloder}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)








def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(listofimages)
encodeListKnownWithIds = [encodeListKnown, uniqueids,names]
print(encodeListKnownWithIds)
print("Encoding Complete")


#pickleing the file 
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

