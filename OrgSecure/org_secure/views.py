import base64
import io
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np 
from PIL import Image
from deepface import DeepFace

from django.conf import settings 
from .models import Person 
from .api_client import ApiClient 
from .creators.encryption_creator import EncryptionCreatorImpl
from .creators.hash_creator import HashingCreatorImpl
from .utils.model_utils import split_face_embedding , edite_image 
from .max_heap.max_heap import MinHeap
# Create your views here.

model = DeepFace.build_model(settings.MODEL_NAME)
hash = HashingCreatorImpl().create()
encryptor = EncryptionCreatorImpl().create()
api_cliant = ApiClient()

def index(request):
    return render(request, 'identify_people.html')



class login(APIView):
    def post(self,request ):
        try:
            response = api_cliant.login()
            return Response({'message': 'log  successfully.'}, status=status.HTTP_201_CREATED)
        except  Exception as err:
            return Response({'error': err}, status=status.HTTP_400_BAD_REQUEST)

        
class ProcessImageView(APIView):
   
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        # Open the image directly from the uploaded file
        try:

            with Image.open(image_file) as img:

                img = np.asarray(img)
                img = np.copy(img)
                results  = DeepFace.represent(img, model_name=settings.MODEL_NAME, enforce_detection=False)

                embeddings , faces_area = split_face_embedding(results)

                for embedding , face_area in zip(embeddings ,faces_area) :

                    max = MinHeap()
                    response = api_cliant.get_candidates(embedding=embedding , encryptor= encryptor , hasher= hash)
                    response_data = response.json()
                    resalts = response_data['result']
                    print("got result")
                    for person_id, distance in zip(resalts['id'], resalts['dis']):
                        distance = encryptor.read_received_data(distance)
                        distance = np.sum(np.abs(encryptor.decrypt(distance)))
                        print(distance)
                        max.add(distance=distance, index= person_id )
                    distance , person_id = max.get_smallest()
                    person = Person.objects.get(id = person_id)
                    print ( person)
                    img = edite_image(img , face_area , str(person))
                img_pil = Image.fromarray(img)  # Convert numpy array back to PIL Image
            img_bytes = io.BytesIO()  # Create a bytes buffer
            img_pil.save(img_bytes, format='JPEG')  # Save the image to the buffer
            img_bytes.seek(0)  # Move to the beginning of the buffer
            image1_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
            response_data = {
            'image': f'data:image/png;base64,{image1_base64}',
            }
            # Return the image in the response
            return JsonResponse(response_data)

        except Exception as e:
            print( str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

