import os
import cv2
from django.core.management.base import BaseCommand
from deepface import DeepFace 
from django.conf import settings 
from ...creators.encryption_creator import EncryptionCreatorImpl
from ...creators.hash_creator import HashingCreatorImpl
from ...api_client import ApiClient
from ...models import Person 

class Command(BaseCommand):
    help = 'this command is to Initialize the data set in poth apps ( the pepole name in this app and the discription vectors in the BioEncryptService app )'
    def handle(self, *args, **kwargs):

        def process_images_in_folder(folder_path):
            encryptor = EncryptionCreatorImpl().create()
            hash = HashingCreatorImpl().create()
            hash.Initialize()
            DeepFace.build_model(settings.MODEL_NAME)
            api_cliant = ApiClient()
            api_cliant.register(api_cliant)
            api_cliant.login(api_cliant)
            api_cliant.send_hashing(hash)
            api_cliant.send_public_key(encryptor)
            i=0
            for subdir, _, files in os.walk(folder_path):
                i+=1 
                print( f"wrking on person number {i} from 200")

                subfolder_name = os.path.basename(subdir)
                first_name, last_name = subfolder_name.split('_', 1) if '_' in subfolder_name else (subfolder_name, '')
                person = Person()
                person_id = person.save_person(firstname=first_name, lastname=last_name).id
                print ("id" ,  person_id )
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(subdir, file)
                        image = cv2.imread(image_path)
                        try:
                            faces =  DeepFace.represent(image, model_name='Facenet')
                        except Exception:
                            continue
                        for face in faces:
                            embedding = face['embedding']
                            response = api_cliant.add_face(id=person_id , final=False , embedding=embedding , encryptor=encryptor , hasher=hash )
                            print (response.status_code )
            api_cliant.save_hashing()

        
        # Your command logic here
        folder_path = os.path.join(settings.BASE_DIR, 'test_1')
        print ( folder_path )
        process_images_in_folder(folder_path)
        self.stdout.write(self.style.SUCCESS('Command executed successfully!'))




