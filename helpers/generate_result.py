from globals import EMAIL_PASSWORD, EMAIL_SENDER
from helpers.AIChat import AIChat
from helpers.EmailSender import EmailSender
from models.Group import Group
from models.User import User
from schemas import OpenaiSettingsSchema
from db import db

HTML_BODY_EMAIL = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Final Destination</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #F4F1E1;
            color: #3E4C59;
        }
        .container {
            width: 100%;
            max-width: 700px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            position: relative;
        }
        .header {
            background-color: #28325e;
            color: #ffffff;
            text-align: center;
            padding: 50px 20px;
            position: relative;
        }
        .header h1 {
            font-size: 48px;
            margin: 0;
            font-weight: bold;
            letter-spacing: 1px;
        }
        .header .wave {
            position: absolute;
            bottom: -20px;
            left: 0;
            width: 100%;
            height: 60px;
            background: #F4F1E1;
            clip-path: ellipse(50% 50% at 50% 50%);
        }
        .destination {
            padding: 40px 20px;
            text-align: center;
            background-color: #F4F1E1;
            color: #3E4C59;
            position: relative;
        }
        .destination h2 {
            font-size: 56px;
            font-weight: bold;
            color: #31428e;
            text-transform: uppercase;
            margin-bottom: 20px;
            letter-spacing: 3px;
        }
        .destination p {
            font-size: 18px;
            line-height: 1.6;
            max-width: 80%;
            margin: 0 auto;
        }
        .cta {
            background-color: #007BFF;
            color: #ffffff;
            padding: 15px 30px;
            font-size: 20px;
            font-weight: bold;
            text-transform: uppercase;
            border-radius: 50px;
            margin-top: 30px;
            display: inline-block;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }
        .cta:hover {
            background-color: #28325e;
        }
        .footer {
            background-color: #F4F1E1;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            color: #999999;
        }
        .footer a {
            color: #007BFF;
            text-decoration: none;
        }
        .abstract-shapes {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: -1;
            overflow: hidden;
        }
        .abstract-shapes .shape1 {
            position: absolute;
            top: -100px;
            left: -100px;
            width: 300px;
            height: 300px;
            background-color: #28325e;
            border-radius: 50%;
        }
        .abstract-shapes .shape2 {
            position: absolute;
            top: 200px;
            right: -150px;
            width: 400px;
            height: 400px;
            background-color: #F4F1E1;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{place}</h1>
            <div class="wave"></div>
        </div>
        <div class="destination">
            <h3>This destination was chosen because...</h3>
            <p>{response}</p>
            <a href="#" class="cta">View Trip Details</a>
        </div>
        <div class="footer">
            <p>Not interested in this destination? <a href="#">Unsubscribe</a>.</p>
        </div>
        <div class="abstract-shapes">
            <div class="shape1"></div>
            <div class="shape2"></div>
        </div>
    </div>
</body>
</html>
"""


def generate_result(settings: OpenaiSettingsSchema, group:Group, users:list[User | str]) -> str:
    """
    Generate the result, sends the emails and saves the response to the group using AI chat completions.

    Args:
        settings (OpenaiSettingsSchema): The settings for the OpenAI API.
        group (Group): The group object containing group information.
        users (list[User | str]): The list of users or emails to send the email to.

    Returns:
        str: The AI chat completion response.
    """
    sender = EmailSender(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username=EMAIL_SENDER,
        password=EMAIL_PASSWORD,
        use_tls=True,
        default_from=f"Lucid Routes App <{EMAIL_SENDER}>"
    )

    ai_chat = AIChat(sender, settings)
    result = ai_chat.query()

    if isinstance(users, list[User]):
        users = [user.email for user in users]

    destination = result.split(" ")[0].replace("_", " ")

    ai_chat.send_emails(
        subject="The travel plan is ready!",
        to=users,
        body_html=HTML_BODY_EMAIL.replace("{place}", destination).replace("{response}", result.split(" ", 1)[1] if len(result.split(" ")) > 1 else result)
    )

    group.response = result
    db.session.commit()

    return result