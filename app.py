from flask import Flask, render_template
import qrcode
from io import BytesIO
import json
from flask_mail import Mail,Message

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'


data = [
    ['21BCE9067', '21BCE9260', '21BCE7343', '21BCE9789', '21BCE7559', '21BCE9325'],
    ['HARIKA', 'KEERTHI', 'PREETHI', 'RAM', 'SATYA', 'SRUTHI'],
    ['present', 'absent', 'present', 'present', 'absent', 'present']
]



app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'b2d2d9f8f0b815'
app.config['MAIL_PASSWORD'] = 'ead9300e7788a1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)



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

@app.route('/')
def home():
    return render_template('index.html', data=data)

@app.route('/qr')
def qr():
    return render_template('qr.html')

@app.route('/mails')
def mails():
    return render_template('Mails.html')

@app.route('/chat_bot')
def chat_bot():
    return render_template('Chat_bot.html')


@app.route('/mails', methods=['POST'])
def send_email():
     recipient = "reshmasriharika@gmail.com"
     subject = "Test Mail"
     message_body = "This is a satyaaaaa mail"

     msg = Message(subject=subject,sender="reshmasriharika",recipients=[recipient])
     msg.body = message_body

     try:
          mail.send(msg)
          return "Email sent successfully!!!"
     except Exception as e:
          return "Error send email:" + str(e)
        







@app.route('/makeSingleQr', methods=['GET'])
def make_single_qr():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_json)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    image_stream = BytesIO()
    img.save(image_stream, format='PNG')
    image_stream.seek(0)

    return app.response_class(image_stream.read(), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
