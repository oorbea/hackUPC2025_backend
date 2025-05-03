import traceback
from flask import abort

from controllers.OpenaiChatLlmController import OpenaiChatLlmController
from globals import DEFAULT_SYSTEM_PROMPT
from helpers.demands_to_messages import demands_to_messages
from models.Demand import Demand
from schemas import OpenaiSettingsSchema
from openai.types.chat import ChatCompletion


class AIChat:
    """
    AI chat completions operations.
    """
    def query(self, data:OpenaiSettingsSchema = {}) -> str:
        """
        Get AI chat completions.

        Args:
            data (OpenaiSettingsSchema): The optional settings for the OpenAI API.

        Returns:
            str: The AI chat completion response.
        """
        try:
            demands:list[Demand] = Demand.query.filter_by(group_id=data.get('group_id')).all()
            messages = demands_to_messages(demands)
            llm = OpenaiChatLlmController(messages, data, system_prompt=DEFAULT_SYSTEM_PROMPT)
            response:ChatCompletion = llm()
            mess = response.choices[0].message.content

            return mess

        except Exception as e:
            traceback.print_exc()
            abort(500, message="Internal server error.")

