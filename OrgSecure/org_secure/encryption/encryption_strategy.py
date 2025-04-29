from abc import  abstractmethod
import base64
import logging
import tenseal as ts 
import os 
from ..utils.file_utils   import read_data 



class EncryptionStrategy():
    """
    Abstract base class for encryption strategies.
    Provides a common interface for encryption, decryption, and context management.
    Derived classes must implement the `encrypt` and `read_received_data` methods.
    """
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
    
    def decrypt(self, encrypted):
        secret_context = ts.context_from(read_data(self.private_key_file))
        encrypted.link_context(secret_context)
        del secret_context
        return encrypted.decrypt()
    
    def get_context( self ):
        data =  self.context.serialize()
        data = base64.b64encode(data).decode('utf-8')
        return data 