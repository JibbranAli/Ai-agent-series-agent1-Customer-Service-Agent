import smtplib
from email.message import EmailMessage

def send_email(smtp_host, smtp_port, username, password, subject, body, to_addrs, from_addr):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    msg.set_content(body)
    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls()
        s.login(username, password)
        s.send_message(msg)
    return True
