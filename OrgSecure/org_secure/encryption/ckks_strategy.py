import os
import tenseal as ts
import base64
from .encryption_strategy import EncryptionStrategy 
from ..utils.file_utils import read_data , write_data
from django.conf import settings

class CKKSStrategy(EncryptionStrategy ):
    '''
        Approximate Homomorphic Encryption
        a leveled homomorphic encryption scheme,
        which means that addition and multiplication are possible,
        but a limited number of multiplications is possible
    '''
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
            self.context = ts.context(ts.SCHEME_TYPE.CKKS,
                                    poly_modulus_degree = settings.CKKS_PARAM['poly_modulus_degree'],
                                    plain_modulus = settings.CKKS_PARAM['plain_modulus'] ,
                                    coeff_mod_bit_sizes = settings.CKKS_PARAM['coeff_mod_bit_sizes'])
            self.context.generate_galois_keys()
            self.context.global_scale = 2**40
            secret_context = self.context.serialize(save_secret_key = True)
            directory = os.path.dirname(self.private_key_file)
            if not os.path.exists(directory):
                os.makedirs(directory)
            write_data(self.private_key_file, secret_context)
            self.context.make_context_public()
            public_context = self.context.serialize()
            write_data(self.public_key_file, public_context)
   
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
    
