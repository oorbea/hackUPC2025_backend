from controllers.BaseController import BaseController


class LlmController(BaseController):
    """
    LLM Controller class that manages the interaction with the LLM (Language Model).
    It inherits from the BaseController and implements the required methods.
    """
    def __init__(self, settings:dict, system_prompt:str):
        """
        Initialize the LLM controller with settings and system prompt.
        
        :param settings: Dictionary containing settings for the LLM.
        :param system_prompt: The system prompt to be used with the LLM.
        """
        super().__init__()
        self.settings = settings
        self.system_prompt = system_prompt

    def run(self):
        """
        Run the LLM controller. This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")