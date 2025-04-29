from abc import ABC ,abstractmethod
import importlib

from ..encryption.encryption_strategy import EncryptionStrategy
from django.conf import settings


class EncryptionCreator(ABC):
    """
    Abstract base class for creating encryption strategies.
    Derived classes must implement the `create` method.
    """
    
    @abstractmethod
    def create(self) -> EncryptionStrategy:
        """
        Create and return an encryption strategy.

        Returns:
            EncryptionStrategy: An instance of an encryption strategy.
        """
        pass
    
class EncryptionCreatorImpl(EncryptionCreator):
    """
    Concrete implementation of the EncryptionCreator class.
    Creates encryption strategies based on the specified type.
    """
    encryption_strategy = None

    def create(self)  -> EncryptionStrategy:
        """
        Create an encryption strategy.
        Returns:
            EncryptionStrategy: An instance of the specified encryption strategy.

        Raises:
            ValueError: If the encryption type is unknown.
        """
  
        if  EncryptionCreatorImpl.encryption_strategy is None :
            # Dynamically import the module and class
            module_path, class_name = settings.ENCRYPTION_CLASSES[settings.ENCRYPTION_STRATEGY].rsplit('.', 1)
            try:
                module = importlib.import_module(module_path)
                strategy_class = getattr(module, class_name)
            except (ImportError, AttributeError) as e:
                raise ValueError(f"Failed to load encryption strategy: {e}")
            EncryptionCreatorImpl.encryption_strategy = strategy_class()
            

        return EncryptionCreatorImpl.encryption_strategy