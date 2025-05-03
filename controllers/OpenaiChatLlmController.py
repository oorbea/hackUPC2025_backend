import re
from controllers.LlmController import LlmController
from openai import NOT_GIVEN, OpenAI, Stream
from openai.types.chat import ChatCompletionChunk

from schemas import OpenaiSettingsSchema

class OpenaiChatLlmController(LlmController):
    """
    OpenAI Chat LLM Controller class that manages the interaction with the OpenAI Chat LLM.
    """
    def __init__(self, settings: OpenaiSettingsSchema, system_prompt: str):
        if not settings.get('api_key'):
            raise ValueError("API key is required for OpenAI Chat LLM.")
        if not settings.get('base_url'):
            raise ValueError("Base URL is required for OpenAI Chat LLM.")
        
        super().__init__(settings, system_prompt)
        client_params = {
            "api_key": settings.pop('api_key'),
            "base_url": settings.pop('base_url')
        }
        self.client = OpenAI(**client_params)

    def _reasoningModelParamsPreparation(self, params:dict) -> dict:
        
        if not re.match(r"o\d+", params['model']): return params
        
        if params.get('messages', None):
            params['messages'] = [{'role': 'user' if msg['role'] == 'system' else msg['role'], 'content': msg['content']} for msg in params['messages']]
        
        params = {k: v or NOT_GIVEN for k, v in params.items()}
        
        params['max_completion_tokens'] = params.get('max_tokens', NOT_GIVEN)
        params.pop('max_tokens', None)
        
        fixedValues = {
            "temperature": 1,
            "top_p": 1,
            "n": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }
        
        for key, value in fixedValues.items():
            if key in params: params[key] = value
        
        return params

    def run(self, messages:Iterable[ChatCompletionMessageParam]) -> Stream[ChatCompletionChunk]:
        """
        Query the OpenAI Chat LLM with the provided settings and system prompt.
        """
        return self.client.chat.completions.create(stream=True, **self._reasoningModelParamsPreparation(self.settings))