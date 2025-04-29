import tenseal as ts
import base64
from .encryption_strategy import EncryptionStrategy 


    
class CKKSStrategy(EncryptionStrategy ):
    '''
        Approximate Homomorphic Encryption
        a leveled homomorphic encryption scheme,
        which means that addition and multiplication are possible,
        but a limited number of multiplications is possible
    '''
   
    def encrypt(self, plaintext):
        if self.context is None:
            raise ValueError("Context is not initialized. Please call receiveContext first.")
        encrypted = ts.ckks_vector(self.context, plaintext)
        return encrypted
    
    def read_received_data(self, data):
        if self.context is None:
            raise ValueError("Context is not initialized. Please call receivePublicKey first.")
        serialized_vector = base64.b64decode(data)
        data = ts.ckks_vector_from(self.context , serialized_vector)
        return data
    