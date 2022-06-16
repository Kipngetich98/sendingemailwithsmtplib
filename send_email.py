from http import server
from importlib.resources import path
import smtplib
import sys

from email import encoders, header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


def send_email_having_attachment(subject, body_text, emails_to, files_attachment):
    """
    send an email having an attachment
    """
    header =f"content-Disposition", "attachemnt; filename={files_attachment}"

    #extract server and from_addr from config
    host = "smtp.your_isp.com"
    from_addr = "vincent@domain.com"

    #create the message 
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if body_text:
        msg.attach(MIMEText(body_text))

    msg["To"] = ",".join(emails_to)

    attachment = MIMEBase("application", "octet-stream")
    try:
        with open(files_attachment, "rb") as fh:
            data = fh.read()
        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = "Error opening file %s" % files_attachment
        print(msg)
        sys.exit

    emails = emails_to

    server = smtplib.SMTP(host)
    server.sendmail(from_addr,emails,msg.as_string())
    server.quit()


    if __name__ == "__main__":
        emails = ["vincent@some_domain.org","kirui@some_domain.org"]

        subject ="Test email with attachment from python"
        body_text = "This email contains the attachment"
        path = "some_path/to/file"
        send_email_having_attachment(subject,body_text,emails,path)
