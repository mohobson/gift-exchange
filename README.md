Secret Santa

This program is designed to automate the name drawing process, ensuring that couples cannot pick each other's names.

To start, fill out the participants excel sheet with the names and email addresses of each participant. The emails can be used to anonymously notify each participant of what name they received. We will set this up in the next step. First, if there are any couples within the group that should be excluded from gifting one another, list them in the 'couples' tab of the excel sheet.

To enable the email service, you will need to create an account with Sendgrid. It's quick and easy, see the link below to get started!

https://sendgrid.com/resource/setting-up-your-email-infrastructure-with-twilio-sendgrid/

Once you have a sendgrid API key, you can create an environment variable for the key. In your terminal, type the command below, replacing x with your API key.

export SENDGRID_API_KEY=x

You will also need to create an environment variable for your email address used to send emails from sendgrid. Type the command below in the terminal, replacing the fake email address with your own.

export fromaddr=fakeeemailaddress@gmail.com

Now you should be all set up! Run the drawing.py file and everyone should receive an email with the name they were assigned.
