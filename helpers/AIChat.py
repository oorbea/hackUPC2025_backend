import traceback
from typing import List, Optional, Union
from flask import abort

from controllers.OpenaiChatLlmController import OpenaiChatLlmController
from globals import DEFAULT_SYSTEM_PROMPT
from helpers.EmailSender import EmailSender
from helpers.demands_to_messages import demands_to_messages
from models.Demand import Demand
from models.Group import Group
from schemas import OpenaiSettingsSchema
from openai.types.chat import ChatCompletion


class AIChat:
    """
    AI chat completions operations.
    """
    def __init__(self, email_sender:EmailSender, settings: OpenaiSettingsSchema):
        """
        Initialize the AI chat with the email sender and settings.

        Args:
            email_sender (EmailSender): The email sender instance.
            settings (OpenaiSettingsSchema): The settings for the OpenAI API.
        """
        self.email_sender = email_sender
        self.settings = settings

    def query(self, group:Group) -> str:
        """
        Get AI chat completions.

        Args:
            data (OpenaiSettingsSchema): The optional settings for the OpenAI API.

        Returns:
            str: The AI chat completion response.
        """
        try:
            demands:list[Demand] = Demand.query.filter_by(group_id=group.id)
            messages = demands_to_messages(demands)
            llm = OpenaiChatLlmController(messages, self.settings, system_prompt=DEFAULT_SYSTEM_PROMPT.replace("{group_name}", group.name)).replace("{group_description}", group.description)
            response:ChatCompletion = llm()
            mess = response.choices[0].message.content

            return mess

        except Exception as e:
            traceback.print_exc()
            abort(500, message="Internal server error.")

    def send_emails(
            self,
            subject: str,
            to: Union[str, List[str]],
            body_text: Optional[str] = None,
            body_html: Optional[str] = None,
            cc: Optional[Union[str, List[str]]] = None,
            bcc: Optional[Union[str, List[str]]] = None,
        ) -> None:
        """
        Send emails using the email sender.
        """
        self.email_sender.send_email(
            subject=subject,
            to=to,
            body_text=body_text,
            body_html=body_html,
            cc=cc,
            bcc=bcc
        )