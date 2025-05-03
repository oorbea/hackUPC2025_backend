from helpers.AIChat import AIChat
from helpers.EmailSender import EmailSender
from schemas import OpenaiSettingsSchema


def generate_result(settings: OpenaiSettingsSchema) -> str:
    """
    Generate the result using AI chat completions.
    """
    sender = EmailSender(
        smtp_server="smtp.example.com",
        smtp_port=587,
        username="no-reply@example.com",
        password="yourpassword",
        use_tls=True,
        default_from="My App <no-reply@example.com>"
    )

    ai_chat = AIChat(sender, settings)