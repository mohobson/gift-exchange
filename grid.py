import os

def sendgrid_email(toaddr, fromaddr, subject, name):

    import base64
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
    
    from dotenv import load_dotenv
    load_dotenv()

    message = Mail(
        to_emails=toaddr,
        subject=subject,
        from_email=fromaddr,
        html_content='<strong>Ho Ho Ho. Get a ~$50 gift for ' + str(name) + '.</strong>'
    )

    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print('')
        print(e.message)

