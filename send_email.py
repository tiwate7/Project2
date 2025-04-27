import smtplib
from email.message import EmailMessage

from_email_addr = "1607629453@qq.com"  
from_email_pass = "lysqscnihapsiiej"  
to_email_addr = "18951836837@163.com"  

msg = EmailMessage()

body = "Hello from Raspberry Pi"
msg.set_content(body)

msg['From'] = from_email_addr
msg['To'] = to_email_addr

msg['Subject'] = 'TEST EMAIL'

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    
    
    server.login(from_email_addr, from_email_pass)
    
    server.send_message(msg)
    print('Email sent successfully！')
    
except Exception as e:
    print(f'Sending failed: {str(e)}')
    
finally:
    if 'server' in locals():
        server.quit()
