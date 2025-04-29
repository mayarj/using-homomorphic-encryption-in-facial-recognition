from abc import  abstractmethod
import base64
import logging
import tenseal as ts 
import os 
from ..utils.file_utils   import read_data  , write_data
from django.conf import settings
logger = logging.getLogger('secure_face_reteval')

class EncryptionStrategy():
    """
    Abstract base class for encryption strategies.
    Provides a common interface for encryption, decryption, and context management.
    Derived classes must implement the `encrypt` and `read_received_data` methods.
    """

    def __init__(self, ID : int ):
        """
        Initialize the encryption strategy.

        Args:
            ID (int): Unique identifier for the encryption context.
                      Used to generate the public key file path.
        """
        self.public_key_file =f'{settings.KEY_FILE}_{ID}.txt'
        self.context = None
        context = read_data(self.public_key_file)
        if context is not None :
            self.context = ts.context_from(context)
        else :
            logger.warning(f"No context file found at {self.public_key_file}. A new context will be created when a public key is received.")
    
    @abstractmethod
    def encrypt(self, plaintext):
        """
        Encrypt the given plaintext.

        Args:
            plaintext: Data to be encrypted.

        Returns:
            Encrypted data.
        """
        pass

    @abstractmethod
    def read_received_data(self, data):
        """
        Deserialize and cast it to its proper format.

        Args:
            data: Serialized and encrypted data.

        Returns:
            Decrypted data.
        """
        pass

    def receiveContext(self, public_data):
        """
        Receive and initialize the encryption context from public key data.

        Args:
            public_data (dict): Dictionary containing the public key.

        Raises:
            ValueError: If the 'public_key' field is missing in public_data.
        """

        if 'public_key' not in public_data:
            raise ValueError("Public data must contain a 'public_key' field.")
        data = public_data['public_key']
        serialized_data= base64.b64decode(data)
        self.context = ts.context_from(serialized_data)
        self.context.make_context_public()
        public_context = self.context.serialize()
        os.makedirs(os.path.dirname(self.public_key_file), exist_ok=True)
        write_data(self.public_key_file, public_context)


    def prepare_data_to_send(self, data):
        """
        Serialize and encode data for transmission.

        Args:
            data: Data to be serialized and encoded.

        Returns:
            Base64-encoded string representation of the data.
        """
        data = data.serialize()
        data = base64.b64encode(data).decode('utf-8') # for safe transmission over networks
        return data
    
    def calculate_distance(self, vector1, vector2):
        """
        Calculate the distance between two encrypted vectors.

        Args:
            vector1: First encrypted vector.
            vector2: Second encrypted vector.

        Returns:
            Base64-encoded string representation of the distance.
        """
        vector1 = self.read_received_data(vector1)
        vector2 = self.read_received_data(vector2)
        return self.prepare_data_to_send(vector1 - vector2)
