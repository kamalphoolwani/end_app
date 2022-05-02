from config import mail, GMAIL_ID

def email_service(user_email, email_title, body):
        # msg = Message(email_title, sender = SENDER_EMAIL, recipients = [user_email])
        # msg.body = "Hello, Reset your account using this url: " + 'http://localhost:5000' + '/user/pass_reset' + '/%d'%(user_id)
        # mail.send(msg)
    print("Sending mail...")
    msg = mail.send_message(
        email_title,
        sender=GMAIL_ID,
        recipients=[user_email],
        body = body
    )