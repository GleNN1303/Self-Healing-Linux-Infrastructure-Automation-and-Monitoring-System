import yagmail

def send_alert(subject, message):

    yag = yagmail.SMTP(
        "supriyakumar817@gmail.com",
        "YOUR_16_CHARACTER_APP_PASSWORD"
    )

    yag.send(
        to="supriyakumar817@gmail.com",
        subject=subject,
        contents=message
    )
