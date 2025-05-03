from globals import EMAIL_PASSWORD, EMAIL_SENDER
from helpers.AIChat import AIChat
from helpers.EmailSender import EmailSender
from schemas import OpenaiSettingsSchema


def generate_result(settings: OpenaiSettingsSchema) -> str:
    """
    Generate the result using AI chat completions.
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