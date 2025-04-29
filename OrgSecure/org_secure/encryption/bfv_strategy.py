import os
import tenseal as ts
import base64
import numpy as np
from .encryption_strategy import EncryptionStrategy 
from django.conf import settings
from ..utils.file_utils import read_data , write_data

class BFVStrategy(EncryptionStrategy):
    def __init__(self ):
        """
        Initialize the encryption strategy.
        """

        self.public_key_file =f'{settings.KEY_FILE}_public.txt'
        self.private_key_file=f'{settings.KEY_FILE}_private.txt'
        self.context = None
        context = read_data(self.public_key_file)
        if context is not None :
            self.context = ts.context_from(context)
        else :
            self.context = ts.context(ts.SCHEME_TYPE.BFV,
                                      poly_modulus_degree=settings.BFV_PARMA['poly_modulus_degree'],
                                      plain_modulus =settings.BFV_PARMA['plain_modulu'])
            self.context.generate_galois_keys()
            self.context.global_scale = 2**20
            secret_context = self.context.serialize(save_secret_key = True)
            directory = os.path.dirname(self.private_key_file)
            if not os.path.exists(directory):
                os.makedirs(directory)
            write_data(self.private_key_file, secret_context)
            self.context.make_context_public()
            public_context = self.context.serialize()
            write_data(self.public_key_file, public_context)

    def encrypt(self, plaintext: np.array):
        if self.context is None:
            raise ValueError("Context is not initialized. Please call receiveContext first.")
        plaintext = settings.BFV_PARMA['scale'] * plaintext
        encrypted = ts.bfv_vector(self.context, plaintext)
        return encrypted
    
    def read_received_data(self, data):
        if self.context is None:
            raise ValueError("Context is not initialized. Please call receiveContext first.")
        serialized_vector = base64.b64decode(data)
        data = ts.bfv_vector_from(self.context , serialized_vector)
        return data