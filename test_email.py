import smtplib
from email.mime.text import MIMEText

# Type these directly for this test — no environment variables yet.
# Use your PERSONAL Gmail account, not a college/work account.
EMAIL_ADDRESS = "jerlinmercy1801@gmail.com"      # <-- replace with your personal Gmail
EMAIL_PASSWORD = "vvcclstttakvwmqd"             # <-- replace with your 16-char app password, NO SPACES

msg = MIMEText("This is a test email from my ticketing system project.")
msg['Subject'] = "Test Email"
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS   # sending to yourself for the test

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    print("Sent successfully! Check your inbox.")
except Exception as e:
    print("FAILED:", e)