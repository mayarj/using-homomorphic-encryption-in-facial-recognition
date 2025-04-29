import os
import cv2
from django.test import TestCase
import numpy as np
from .api_client import ApiClient 
from .creators.hash_creator import HashingCreatorImpl
from .creators.encryption_creator import EncryptionCreatorImpl
from .max_heap.max_heap import MinHeap
from django.conf import settings
from deepface import DeepFace 
from .models import Person
DeepFace.build_model(settings.MODEL_NAME)
# Create your tests here.
class TestApiCliant(TestCase):
    def setUp(self):
        self.api_cliant = ApiClient()
        
    
    # def testhashsend(self):
    #     hash = HashingCreatorImpl().create()
    #     hash.Initialize()
    #     response = self.api_cliant.send_hashing(hash)
    #     print ( "hashing was sent ")
    #     self.assertEqual(response.status_code, 200)

    # def testEncryptionsend (self ):
    #     print ( 'testing send public key ' )
    #     encryptor = EncryptionCreatorImpl().create()
    #     response = self.api_cliant.send_public_key(encryptor)
    #     self.assertEqual(response.status_code, 200)

    def testfull ( self ): 
        
        hash = HashingCreatorImpl().create()
        encryptor = EncryptionCreatorImpl().create()
        image_path = os.path.join(settings.BASE_DIR, 'test_1/Adisai_Bodharamik/Adisai_Bodharamik_0001.jpg')
        # Read the image
        image = cv2.imread(image_path)
        faces =  DeepFace.represent(image, model_name='Facenet')
        for face in faces :
            max = MinHeap()
            embedding = face['embedding']
            response = self.api_cliant.get_candidates(embedding=embedding , encryptor= encryptor , hasher= hash)
            print ("getting candidates status code " , response.status_code )
            response_data = response.json()
            resalts = response_data['result']
            print ( resalts['id'])
            for person_id, distance in zip(resalts['id'], resalts['dis']):

                distance = encryptor.read_received_data(distance)

                distance = np.sum(np.abs(encryptor.decrypt(distance)))
                # print ( dis )
                max.add(distance=distance, index= person_id )




        