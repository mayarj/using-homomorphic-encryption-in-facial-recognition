from abc import ABC ,abstractmethod
import importlib
import logging
from ..encryption.encryption_strategy import EncryptionStrategy
from django.conf import settings
logger = logging.getLogger('secure_face_reteval')

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
    

    def create(self, ID:int ,  encryption_type: str = 'ckks' )  -> EncryptionStrategy:
        """
        Create an encryption strategy.

        Args:
            ID (int): Unique identifier for the encryption strategy.
            encryption_type (str, optional): Type of encryption strategy to create.
                                            Defaults to the first type in ENCRYPTION_CLASSES.

        Returns:
            EncryptionStrategy: An instance of the specified encryption strategy.

        Raises:
            ValueError: If the encryption type is unknown.
        """

        # Check if the encryption type is valid
        if encryption_type in settings.ENCRYPTION_CLASSES.keys():
            # Dynamically import the module and class
            module_path, class_name = settings.ENCRYPTION_CLASSES[encryption_type].rsplit('.', 1)
            try:
                module = importlib.import_module(module_path)
                strategy_class = getattr(module, class_name)
            except (ImportError, AttributeError) as e:
                raise ValueError(f"Failed to load encryption strategy: {e}")
            # Create and return an instance of the encryption strategy
            encryption_strategy = strategy_class(ID)
            logger.info(f"Creating encryption strategy of type: {encryption_type}")
            return  encryption_strategy
        else:
            raise ValueError(f"Unknown encryption type: {encryption_type}")