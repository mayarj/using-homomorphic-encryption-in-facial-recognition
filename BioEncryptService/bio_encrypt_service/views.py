import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import EncryptedEmbedding
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from django.conf import settings


logger = logging.getLogger('bio_encrypt_service')

class COMMONLOGIC(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return request

class RegisterView(APIView):
    """
    View for user registration.
    Allows unauthenticated users to register and create a new account.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user registration.

        Args:
            request: The HTTP request containing user data.

        Returns:
            Response: HTTP response with user data or errors.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User registered: {serializer.data['username']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """
    View for user login.
    Allows unauthenticated users to log in and obtain JWT tokens.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        """
        Handle user login.

        Args:
            request: The HTTP request containing login credentials.

        Returns:
            Response: HTTP response with JWT tokens or errors.
        """
        response = super().post(request, *args, **kwargs)
        logger.info(f"User logged in: {request.data.get('username')}")
        return response


class ReceivePublicKeyView(APIView):
    """
    View for receiving a public key from the client.
    Allows authenticated users to send their public key for encryption.
    """

    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        Handle the receipt of a public key.

        Args:
            request: The HTTP request containing the public key.

        Returns:
            Response: HTTP response indicating success or failure.
        """
        try:
            public_key = request.data
            request.CkksInstance.receiveContext(public_key)
            logger.info(f"Public key received from user: {request.user.id}")
            return Response({'message': 'Public key received successfully.'}, status=status.HTTP_200_OK)
        except KeyError:
            logger.error("Public key is required.")
            return Response({'error': 'Public key is required.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error receiving public key: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReceiveHashing(APIView):
    """
    View for receiving LSH data from the client.
    Allows authenticated users to send their LSH data for hashing.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        Handle the receipt of LSH data.

        Args:
            request: The HTTP request containing LSH data.

        Returns:
            Response: HTTP response indicating success or failure.
        """
        try:
            Hashing_data = request.data['hashing_data']
            request.LshInstance.receive_model(Hashing_data)
            logger.info(f"LSH data received from user: {request.user}")
            print ( "Hashing_data" , Hashing_data)
            return Response({'message': 'LSH received successfully.'}, status=status.HTTP_200_OK)
        except KeyError:
            logger.error("LSH data key is required.")
            return Response({'error': 'LSH data key is required.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error receiving LSH data: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SaveHashing(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            request.LshInstance.save_model()
            logger.info("LSH data is saved .")
            return Response({'message': 'LSH was saved successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error receiving LSH data: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AddFace(APIView):
    """
    View for adding a face embedding to the system.
    Allows authenticated users to add encrypted face embeddings.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        Handle the addition of a face embedding.

        Args:
            request: The HTTP request containing the encrypted embedding and metadata.

        Returns:
            Response: HTTP response indicating success or failure.
        """
        try:
            encrypted_data = request.data['encrypted_data']
            point_hash = request.data['point_hash']
            point_identification = request.data['point_identification']  
            final = request.data['final']

            # Update hashing instance
            request.LshInstance.update_hashing( point_hashes =point_hash, id = point_identification ,  final =final )

            # Read received data (ensure this method exists)
            encrypted_embedding = request.CkksInstance.read_received_data(encrypted_data)  # Corrected variable name
            encrypted_embedding = request.CkksInstance.prepare_data_to_send(encrypted_embedding)

            # Save encrypted data
            ckks_instance = EncryptedEmbedding()
            ckks_instance.save_encrypted(encrypted_embedding, point_identification, request.user)

            logger.info(f"Face added successfully for user: {request.user.id}")
            return Response({'message': 'Face added successfully.'}, status=status.HTTP_201_CREATED)
        except KeyError as e:
            logger.error(f"Missing key: {str(e)}")
            return Response({'error': f'Missing key: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error adding face: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Knerast(APIView):
    """
    View for retrieving the nearest neighbors of a face embedding.
    Allows authenticated users to query the system for similar faces.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle the retrieval of nearest neighbors.

        Args:
            request: The HTTP request containing the query embedding.

        Returns:
            Response: HTTP response with the nearest neighbors or errors.
        """
        try:
            encrypted_data = request.data['encrypted_data']
            point_hash = request.data['point_hash']
            # Get nearest identifications using LSH
            identifications = request.LshInstance.get_k_nearest(point_hash)
           
            # Retrieve encrypted embeddings for the nearest identifications
            encrypted_embeddings = EncryptedEmbedding.objects.filter(
                user_id=request.user.id,
                identification__in=identifications
            ).values_list('identification', "embedding")
            # Calculate distances using homomorphic operations
            result = {
                'id':[],
                'dis':[],
            }
            for identification, encrypted_embedding_db in encrypted_embeddings:
                distance = request.CkksInstance.calculate_distance(
                    encrypted_data, encrypted_embedding_db
                )
                result['id'].append(identification)
                result['dis'].append(distance)
            logger.info(f"Nearest identifications retrieved for user: {request.user.id}")
            return Response({'result': result}, status=status.HTTP_200_OK)
        except KeyError as e:
            logger.error(f"Missing key: {str(e)}")
            return Response({'error': f'Missing key: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error retrieving nearest identifications: {str(e)}")
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
