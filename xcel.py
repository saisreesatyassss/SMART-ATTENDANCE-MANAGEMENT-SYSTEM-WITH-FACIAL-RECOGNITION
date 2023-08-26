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
for key, value in firebase_data.items():
    data_list.append({"Key": key, "Value": value})

df = pd.DataFrame(data_list)

# Export DataFrame to an Excel file
output_file = "firebase_data.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"Data exported to {output_file}")
