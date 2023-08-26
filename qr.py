import qrcode
from PIL import Image
import json

# Sample data
data = [
    ['21BCE9067', '21BCE9260', '21BCE7343', '21BCE9789', '21BCE7559', '21BCE9325'],
    ['HARIKA', 'KEERTHI', 'PREETHI', 'RAM', 'SATYA', 'SRUTHI'],
    ['present', 'absent', 'present', 'present', 'absent', 'present']
]

# Create a list of dictionaries to store student data
students = []
for student_id, student_name, status in zip(*data):
    student = {
        "Student ID": student_id,
        "Name": student_name,
        "Status": status
    }
    students.append(student)

# Convert the list of dictionaries to JSON format
data_json = json.dumps(students, indent=4)

# Generate a QR code with the JSON data
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data_json)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white")

# Display the QR code image
qr_img.show()

# You can save the QR code to a file if needed
# qr_img.save("data_qr.png")
 

 
