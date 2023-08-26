import cv2
import os
import numpy as np
import pickle
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://facerecognition-f2f3c-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognition-f2f3c.appspot.com"  # gs://  -remove-  facerecognition-f2f3c.appspot.com

})


bucket = storage.bucket()

cap = cv2.VideoCapture(0)
#  0 for the built-in webcam and 1 for the external camera
cap.set(3,640)
cap.set(4,480)

bgimage=cv2.imread("images/background.png")



# Importing the mode images into a list
folderModePath = 'images/modes'
modePathinList = os.listdir(folderModePath)
# print(modePathinList)

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds,names = encodeListKnownWithIds
print(names)
print(studentIds)
print("Encode File Loaded")

imgModeList = []
for path in modePathinList:
    imagepath=os.path.join(folderModePath, path)
    imgModeList.append(cv2.imread(imagepath))

    #os.path.join is for to join path it will a / in between its better to use for platform indenpetne
# print(len(imgModeList))
modeType = 0
counter = 0
id = -1
imgStudent = []
studentEntryExit = {}  # Dictionary to store entry and exit times
total_duration_text = "0 seconds"
total_duration = None  
total_seconds = 0

while True:
    success,img=cap.read() # success is boolean img is numpyarry with imag etails like height weight frames channels 
    # (height, width, 3) shape is jpg image for imread returs same

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)  ## for bounding boxes 
    # print(faceCurFrame)
    
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    # #face_encodings of new face which is in cam uner current frame
    
    bgimage[162:162 + 480, 55:55 + 640]=img
    bgimage[44:44 + 633, 808:808 + 414]=imgModeList[modeType]
    if faceCurFrame:
    # loop through encodeCurFrame an compare with generate encodings
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)#encodeListKnown from unziping pickel file
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                #lower istance better match itslike simialrties between faces
                print("matches", matches)
                print("faceDis", faceDis)

                matchIndex = np.argmin(faceDis)#take the main of the face_distance
                # print("Match Index", matchIndex)


                if matches[matchIndex]: #matchIndex are true if 1 is true or not     ture or not from matches
                    # print(studentIds[matchIndex])# printng the Ids of face matche
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1# 55 162 cam image staring from there 
                    bgimage = cvzone.cornerRect(bgimage, bbox, rt=0)

                    id = studentIds[matchIndex]
                    name=names[matchIndex]
                    if id not in studentEntryExit:
                       studentEntryExit[id] = {'entry': datetime.now(), 'exit': None}
                    else:
                       if id in studentEntryExit:
                          studentEntryExit[id]['exit'] = datetime.now()
                          total_duration = studentEntryExit[id]['exit'] - studentEntryExit[id]['entry']
                          if total_duration:
                              total_seconds = total_duration.total_seconds()
                              print(f"Total Duration: {total_duration}")
                    if counter == 0:
                        cvzone.putTextRect(bgimage, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", bgimage)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1
        if counter != 0:

            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the Image from the storage
                print(id)
                print(name)
                            # Get the Image from the storage
                blob = bucket.get_blob(f'images/faces/{name},{id}.jpg')
                print(blob)
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                print("Image Shape:", imgStudent.shape)
                if total_duration is not None:
                    total_seconds = total_duration.total_seconds()
                    if total_seconds >= 60 and total_seconds < 3600:
                        total_minutes = total_seconds / 60
                        total_duration_text = f"{total_minutes:.2f} minutes"
                    elif total_seconds >= 3600:
                        total_hours = total_seconds / 3600
                        total_duration_text = f"{total_hours:.2f} hours"
                    else:
                        total_duration_text = f"{total_seconds:.2f} seconds"

                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    date = datetime.now().strftime("%Y-%m-%d")
                    att_ref = db.reference(f'Attendance/{date}')
                    absentees_ref = att_ref.child('Absentees')
                    presentees_ref = att_ref.child('Presentees')

                    for student_id, student_data in studentEntryExit.items():
                        if student_data['exit'] is not None:
                            student_info = db.reference(f'Students/{id}').get()
                            if (student_data['exit'] - student_data['entry']).total_seconds() > 30:
                                 
                                #  absentee_ref = absentees_ref.child(id)
                                #  absentee_ref.update({
                                #      'name': student_info['name'],
                                #      'total_duration': total_duration_text
                                #  })
                                #  presentees_ref.child(id).delete()
                                presentee_ref = presentees_ref.child(id)
                                presentee_ref.set({
                                    'name': student_info['name'],
                                    'total_duration': total_duration_text
                                })
                                # absentees_ref.child(id).delete()
                            # else:
                                # absentee_ref = absentees_ref.child(id)
                                # absentee_ref.update({
                                #      'name': student_info['name'],
                                #      'total_duration': total_duration_text
                                #  })
                                # presentees_ref.child(id).delete() 
                                # presentee_ref = presentees_ref.child(id)
                                # presentee_ref.set({
                                #     'name': student_info['name'],
                                #     'total_duration': total_duration_text
                                # })
                                # absentees_ref.child(id).delete()

                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    bgimage[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                bgimage[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(bgimage, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(bgimage, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(bgimage, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(bgimage, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(bgimage, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(bgimage, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(bgimage, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    bgimage[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    bgimage[44:44 + 633, 808:808 + 414] = imgModeList[modeType]



    else:
        modeType = 0
        counter = 0





    # cv2.imshow("hello",imgS) 
    cv2.imshow("Face Attendance", bgimage)
    if cv2.waitKey(1)  & 0xFF == ord('q'):
      break# Wait for a key press (any key) and then close the window


cap.release()
cv2.destroyAllWindows() # Close all OpenCV windows