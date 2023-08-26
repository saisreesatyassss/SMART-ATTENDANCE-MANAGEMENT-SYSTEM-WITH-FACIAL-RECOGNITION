import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-f2f3c-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognition-f2f3c.appspot.com"
})

# Retrieve data from Firebase
ref = db.reference("Attendance")
firebase_data = ref.get()

# Convert data to a pandas DataFrame
data_list = []
for date, attendance_data in firebase_data.items():
    for student_id, status in attendance_data.get("Presentees", {}).items():
        data_list.append({"ID": student_id, "Date": date,"Status": "Present"})
    for student_id, status in attendance_data.get("Absentees", {}).items():
        data_list.append({"ID": student_id, "Date": date, "Status": "Absent"})

df = pd.DataFrame(data_list)

# Export DataFrame to a CSV file
output_file = "attendance_data.csv"
df.to_csv(output_file, index=False)

print(f"Data exported to {output_file}")