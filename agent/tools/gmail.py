import os
from email.message import EmailMessage
import ssl
import smtplib
# import requests
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()

email_sender = "info@dalongo.com"
email_pwd = os.environ['GMAIL_KEY'].replace('_', ' ')

email_receiver = "pablo.masior@gmail.com"

def _send_mail(email_receiver,query, pdf):
    try:
        subj = f"Your Startup idea report"
        body = f"""
Hello user!

Here is your report.

Enjoy! 😀
        """

        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_data = pdf_buffer.getvalue()  # Get the byte content of the PDF
        pdf_buffer.close()
        
        em = EmailMessage()
        em['From'] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subj
        em.set_content(body)
        em.add_attachment(pdf_data, maintype="application", subtype="pdf", filename=f"{subj}.pdf")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_pwd)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        return f"Success: sent email to {email_sender}"
    except: pass