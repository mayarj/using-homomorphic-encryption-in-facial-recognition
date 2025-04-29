import base64
from django.test import TestCase
import tenseal as ts 
import numpy as np 
from ..encryption.ckks_strategy import CKKSStrategy
from ..encryption.bfv_strategy import BFVStrategy
from ..creators.encryption_creator import EncryptionCreatorImpl




class TestEncriptionStrategy(TestCase):
    def setUp(self):
        self.creator = EncryptionCreatorImpl() ; 
        encription_strategy = self.creator.create(1 , 'CKKS') 
        context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, plain_modulus=-1, coeff_mod_bit_sizes=[60, 40, 40, 60])
        context.generate_galois_keys()
        context.global_scale = 2**40
        secret_context = context.serialize(save_secret_key=True)
        context.make_context_public()
        public_key =context.serialize()
        encription_strategy.receiveContext({'public_key':public_key})
        encription_strategy = self.creator.create(2 , 'BFV') 
        context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=8192,plain_modulus = 256  )
        context.generate_galois_keys()
        context.global_scale = 2**40
        secret_context = context.serialize(save_secret_key=True)
        context.make_context_public()
        public_key =context.serialize()
        encription_strategy.receiveContext({'public_key':public_key})

    def creation(self):
        encription_strategy = self.creator.create(1 , 'CKKS') 
        self.assertIsInstance(encription_strategy ,CKKSStrategy)
        encription_strategy = self.creator.create(2 , 'BFV') 
        self.assertIsInstance(encription_strategy ,BFVStrategy)
    
    

    def CKKS_encrypt(self):
        encription_strategy = self.creator.create(1 , 'CKKS') 
        vector = np.random.randn(128)
        enc_vector = encription_strategy.encrypt(vector)
        self.assertIsInstance(enc_vector  ,ts.tensors.ckksvector.CKKSVector)
        encription_strategy = self.creator.create(2 , 'BFV') 
        enc_vector = encription_strategy.encrypt(vector)
        self.assertIsInstance(enc_vector  ,ts.tensors.ckksvector.BFVVector)

    def test_receive_data(self):
        encription_strategy = self.creator.create(1, 'CKKS') 
        vector = np.random.randn(128)
        enc_vector = encription_strategy.encrypt(vector)
        # Prepare the data to send
        serialized_data = encription_strategy.prepare_data_to_send(enc_vector)
        
        # Simulate receiving the data
        received_data = serialized_data
        
        # Read the received data
        decrypted_vector = encription_strategy.read_received_data(received_data)
        
        # Check if the decrypted vector is an instance of CKKSVector
        self.assertIsInstance(decrypted_vector, ts.tensors.ckksvector.CKKSVector)

