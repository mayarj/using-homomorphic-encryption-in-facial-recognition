

import requests
from django.conf import settings

from .hashing.hashing_strategy import HashingStrategy
import numpy as np
from .encryption.encryption_strategy import EncryptionStrategy


class ApiClient:
    """
    API client for interacting with the organization server.
    Handles user registration, login, and secure face processing operations.
    """

    access_token = None  # Stores the access token for authenticated requests
    refresh_token = None  # Stores the refresh token for token renewal

    def __init__(self):
        """
        Initialize the API client and start the periodic login.

        Args:
            organization_name (str): Name of the organization.
            password (str): Password for the organization.
        """
        self.credentials = settings.USER_CREDENTIALS

        self.login(self)
        

    @staticmethod
    def register(self):
        
        data = self.credentials
        try:
            # Send registration request to the server
            post_response = requests.post(settings.URLS['registering_url'], json=data)
            post_response.raise_for_status()  # Raise an error for bad responses

            # Extract tokens from the response
            response_data = post_response.json()
            access_token = response_data.get('access_token')
            refresh_token = response_data.get('refresh_token')

            if access_token and refresh_token:
                ApiClient.access_token = access_token
                ApiClient.refresh_token = refresh_token
                print("Registration successful. Tokens saved.")
            else:
                print("Registration successful, but no tokens returned.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    @staticmethod
    def login(self):
        """
        Log in an organization and retrieve access and refresh tokens.

        Returns:
            None
        """

        try:
            # Send login request to the server

            
            post_response = requests.post(settings.URLS['login'], json=self.credentials)
            
            post_response.raise_for_status()  # Raise an error for bad responses

            # Extract tokens from the response
            response_data = post_response.json()
            access_token = response_data.get('access')
            refresh_token = response_data.get('refresh')

            if access_token and refresh_token:
                ApiClient.access_token = access_token
                ApiClient.refresh_token = refresh_token
                print (response_data )
                print("Login successful. Tokens saved.")
            else:
                print("Login successful, but no tokens returned.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    @staticmethod
    def send_public_key(encryptor: EncryptionStrategy):
        """
        Send the public key to the server for encryption.

        Args:
            encryptor (EncryptionStrategy): The encryption strategy instance.

        Returns:
            None
        """
        headers = {'Authorization': f'Bearer {ApiClient.access_token}'}
        data = {
            'public_key': encryptor.get_context()  # Get the encryption context
        }

        try:
            # Send the public key to the server
            response = requests.post(settings.URLS['send_public_key'], json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print(f"{response_data}")
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    @staticmethod
    def send_hashing(hasher: HashingStrategy):
        """
        Send the hashing model to the server.

        Args:
            hasher (HashingStrategy): The hashing strategy instance.

        Returns:
            None
        """
        data = { 
            'hashing_data':{}
        }
        data['hashing_data'] = hasher.get_model()  # Get the hashing model
        headers = {'Authorization': f'Bearer {ApiClient.access_token}'}

        try:
            # Send the hashing model to the server
            response = requests.post(settings.URLS['send_hashing'], json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print(f"{response_data}")
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    @staticmethod
    def add_face(id:int, final:bool, embedding: np.array, encryptor: EncryptionStrategy, hasher: HashingStrategy):
        """
        Add a face embedding to the server.

        Args:
            id (int): Unique identifier for the face.
            final (bool): Indicates if this is the final face for the user.
            embedding (np.array): The face embedding to add.
            encryptor (EncryptionStrategy): The encryption strategy instance.
            hasher (HashingStrategy): The hashing strategy instance.

        Returns:
            None
        """
        encrypted_data =  encryptor.encrypt(embedding)
        encrypted_data  = encryptor.prepare_data_to_send(encrypted_data)
        headers = {'Authorization': f'Bearer {ApiClient.access_token}'}
        data = {
            'encrypted_data': encrypted_data ,  # Encrypt the embedding
            'point_hash': hasher.get_point_hash(embedding),  # Get the hash of the embedding
            'point_identification': id,
            'final': final
        }

        try:
            # Send the face data to the server
            response = requests.post(settings.URLS['add_face'], json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print(f"{response_data}")
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
    
    @staticmethod
    def save_hashing():
        headers = {'Authorization': f'Bearer {ApiClient.access_token}'}
        try:
            response = requests.post(settings.URLS['save_hashing'], headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print(f"{response_data}")
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
   
    @staticmethod
    def get_candidates(embedding: np.array, encryptor: EncryptionStrategy, hasher: HashingStrategy):

        """
        Retrieve candidate matches for a face embedding.

        Args:
            embedding (np.array): The face embedding to query.
            encryptor (EncryptionStrategy): The encryption strategy instance.
            hasher (HashingStrategy): The hashing strategy instance.

        Returns:
            None
        """
        encrypted_data =  encryptor.encrypt(embedding)
        encrypted_data  = encryptor.prepare_data_to_send(encrypted_data)
        data = {
            'encrypted_data':  encrypted_data,  # Encrypt the embedding
            'point_hash': hasher.get_point_hash(embedding)  # Get the hash of the embedding
        }
       
        headers = {'Authorization': f'Bearer {ApiClient.access_token}'}

        try:
            # Query the server for candidate matches
            response = requests.get(settings.URLS['get_candidates'], json=data, headers=headers)
            response.raise_for_status()
            
           
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")