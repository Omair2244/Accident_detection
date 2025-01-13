from flask import Flask, render_template, Response
import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from model import load_model, predict_frame

app = Flask(__name__)
model = load_model()  # Load your pre-trained model here

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'muhammadomair678@gmail.com'  
EMAIL_PASSWORD = 'Omair@123'  
RECIPIENT_EMAIL = 'omair.6508@gmail.com'  

def send_email_alert():
    """Send an email alert when an accident is detected."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Accident Detected Alert'
        body = 'An accident has been detected by the system. Please take immediate action.'
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

def generate_frames():
    """Capture live webcam video and process each frame."""
    camera = cv2.VideoCapture(0)  # Open webcam

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Model prediction
            detection_result = predict_frame(model, frame)
            
            if detection_result == "Accident":
                print("Accident detected! Sending email alert...")
                send_email_alert()
            
            # Display detection result on the frame
            cv2.putText(frame, detection_result, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Encode frame for Flask to stream
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

@app.route('/video_feed')
def video_feed():
    """Route for video streaming."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

