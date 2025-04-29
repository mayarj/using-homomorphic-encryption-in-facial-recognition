import numpy as np
import pickle
import os 
from typing import List
from .hashing_strategy import  HashingStrategy
from django.conf import settings

class LSHStrategy( HashingStrategy):
    """
    Implementation of the Locality-Sensitive Hashing (LSH) strategy.
    Uses random projections to hash points into buckets for efficient nearest neighbor search.
    """
    def __init__(   self,
                    n_dimensions: int ,
                    n_tables: int,
                    n_projections: int 
                ):
        """
        Initialize the LSH model.
        :param n_dimensions: Number of dimensions of the data points.
        :param n_tables: Number of hash tables.
        :param n_projections: Number of random projections per hash table.
        :param ID : the ID of the user that created this HASH for his profile 
        """
        self.lshFile = f'{settings.HASHING_DIRECTORY}/LSH.pkl'
        self.n_dimensions = n_dimensions
        self.n_tables = n_tables
        self.n_projections = n_projections
        self.projections = []  # List of random projection matrices
        if os.path.exists(self.lshFile) :
            self.load_model()

    def Initialize(self):
        """
        Initialize the LSH model by generating random projection matrices.
        """
        # Generate random projection matrices for each hash table
        for _ in range(self.n_tables):
            # Random projection matrix of shape (n_projections, n_dimensions)
            projection = np.random.randn(self.n_projections,self.n_dimensions)
            self.projections.append(projection)
        self.save_model()
            
    def hash_point(self, point: np.ndarray, projection: np.ndarray):
        """
        Compute the hash of a point using a given projection matrix.

        Args:
            point (np.ndarray): The point to hash (n-dimensional numpy array).
            projection (np.ndarray): The projection matrix.

        Returns:
            str: The hash as a string (e.g., "1010").
        """
        # Project the point onto the random vectors
        projected = np.dot(projection, point)
        # Quantize the projected values into binary (0 or 1)
        binary_hash = (projected > 0).astype(int)
        # Convert the binary array to a string (e.g., "1010")
        return  ''.join(map(str, binary_hash))
    
    def get_point_hash(self, point: np.ndarray) -> List[str]:
        """
        Compute the hash of a point using the LSH.

        Args:
            point (np.ndarray): The point to hash.

        Returns:
            List[str]: List of hashes (one for each hash table).
        """
        return [self.hash_point(point, projection) for projection in self.projections]
          
    def save_model(self):
        """
        Save the LSH model to disk.
        """
        directory = os.path.dirname(self.lshFile)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(self.lshFile, 'wb') as f:
            pickle.dump({
                'n_dimensions': self.n_dimensions,
                'n_tables': self.n_tables,
                'n_projections': self.n_projections,
                'projections': self.projections,

            }, f)

    def load_model(self ):
        """
        Load the LSH model from disk.
        """
       
        with open(self.lshFile, 'rb') as f:
            data = pickle.load(f)
        
        self.n_dimensions = data['n_dimensions']
        self.n_tables = data['n_tables']
        self.n_projections = data['n_projections']
        self.projections = data['projections']

    def get_model(self):
        data = {
                'n_dimensions': self.n_dimensions,
                'n_tables': self.n_tables,
                'n_projections': self.n_projections,
                'projections': [],
                'hash_tables': []
            }
        return data 
    
    def __str__(self):
        return f"n_dimensions: {self.n_dimensions},n_tables:{ self.n_tables},n_projections: {self.n_projections}"