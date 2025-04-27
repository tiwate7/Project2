#!/usr/bin/env python3

import RPi.GPIO as GPIO
import smtplib
import time
from email.message import EmailMessage
from datetime import datetime

SENSOR_PIN = 4         # GPIO4 (BCM numbering)
CHECK_INTERVAL = 3     # Check interval (hours)
status_map = {
    1: ("Water needed!", "[Alert] Plant needs water"),
    0: ("Water is enough", "[OK] Plant status normal")
}

SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 465
SENDER_EMAIL = "1607629453@qq.com"
SENDER_PASSWORD = "lysqscnihapsiiej"  
RECEIVER_EMAIL = "18951836837@163.com"

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    print("GPIO initialization completed")

def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        full_subject = f"{subject} - {current_time}"
        msg['Subject'] = full_subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully at {current_time}")

    except Exception as e:
        print(f"Email sending failed: {str(e)}")

if __name__ == "__main__":
    try:
        setup_gpio()
        check_interval = CHECK_INTERVAL * 3600  # Convert to seconds
        
        print(f"Plant monitoring system started, reporting every {CHECK_INTERVAL} hours...")
        
        while True:
            current_status = GPIO.input(SENSOR_PIN)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            message, subject = status_map[current_status]
            email_body = f"""\
Detection time: {current_time}
Current status: {message}
Sensor reading: {'Dry' if current_status else 'Wet'}"""
            
            send_email(subject, email_body)
           
            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        GPIO.cleanup()
