from abc import ABC, abstractmethod


class BaseController(ABC):
    """
    Base controller class that defines the interface for all controllers.
    Controllers should inherit from this class and implement the required methods.
    """

    @abstractmethod
    def run(self):
        """
        Run the controller. This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def __call__(self, *args, **kwargs):
        """
        Call the run method when the instance is called.
        """
        return self.run(*args, **kwargs)