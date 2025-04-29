import tenseal as ts
import base64
from .encryption_strategy import EncryptionStrategy 


class BFVStrategy(EncryptionStrategy):
    def encrypt(self, plaintext):
        if self.context is None:
            raise ValueError("Context is not initialized. Please call receiveContext first.")
        encrypted = ts.bfv_vector(self.context, plaintext)
        return encrypted
    
    def read_received_data(self, data):
        if self.context is None:
            raise ValueError("Context is not initialized. Please call receiveContext first.")
        serialized_vector = base64.b64decode(data)
        data = ts.bfv_vector_from(self.context , serialized_vector)
        return data