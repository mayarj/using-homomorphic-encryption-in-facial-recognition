import numpy as np
import pickle
import os 
from typing import List
from .hashing_strategy import  hashingStrategy
from django.conf import settings
class LSHStrategy( hashingStrategy):
    """
    Implementation of the Locality-Sensitive Hashing (LSH) strategy.
    Uses random projections to hash points into buckets for efficient nearest neighbor search.
    """
    def __init__(   self,ID : int  ,
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
        self.lshFile = f'{settings.HASHING_DIRECTORY}/LSH_{ID}.pkl'
        self.n_dimensions = n_dimensions
        self.n_tables = n_tables
        self.n_projections = n_projections
        self.hash_tables = []  # List of hash tables (dictionaries)
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
            self.hash_tables.append({})  

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
    
    def create_hashing(self, points: List[np.ndarray] , ids : np.ndarray):
        """
        Create the LSH index from a list of points.

        Args:
            points (List[np.ndarray]): List of n-dimensional points.
            ids (np.ndarray): List of IDs corresponding to the points.
        """
        
        for j, point in zip(ids, points):
           
            point_hashes = self.get_point_hash(point)
            for i, point_hash in enumerate(point_hashes):
                if point_hash not in self.hash_tables[i]:
                    self.hash_tables[i][point_hash] = []
                self.hash_tables[i][point_hash].append(j)
        self.save_model()
    
    def update_hashing( self , point_hashes , id  , final = False ):
        """
        Update the LSH index with a new point.

        Args:
            point_hashs: Hashes of the new point for each hash table.
            id: ID of the new point.
        """

        for i, point_hash in enumerate(point_hashes):
            # Add the point to the corresponding hash table
          
            if point_hash not in self.hash_tables[i]:
                self.hash_tables[i][point_hash] = []
            self.hash_tables[i][point_hash].append(id)
        if final : 
            self.save_model()

    def get_point_hash(self, point: np.ndarray) -> List[str]:
        """
        Compute the hash of a point using the LSH.

        Args:
            point (np.ndarray): The point to hash.

        Returns:
            List[str]: List of hashes (one for each hash table).
        """
        return [self.hash_point(point, projection) for projection in self.projections]
    
    def get_k_nearest(self, point_hashes: List[str]):
        """
        Find the k-nearest neighbors of a point using its hash.

        Args:
            point_hashes (List[str]): The hash of the query point.

        Returns:
            List of candidate IDs (nearest neighbors).
        """
        candidates = set() 
        
        for i, hash_val in enumerate(point_hashes):
           
            if hash_val in self.hash_tables[i]:
                candidates.update(self.hash_tables[i][hash_val])
        return list(candidates) 
    
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
                'hash_tables': self.hash_tables
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
        self.hash_tables = data['hash_tables']

    def receive_model(self , data):
        """"
        Load the LSH model from serialized data , and save the model.

        Args:
            data: Serialized LSH model data.
        """
        self.n_dimensions = data['n_dimensions']
        self.n_tables = data['n_tables']
        self.n_projections = data['n_projections']
        self.projections = []
        self.hash_tables = []
        for i in range(self.n_projections):
            self.hash_tables.append({})
        self.save_model()
    def __str__(self):
        return f"n_dimensions: {self.n_dimensions},n_tables:{ self.n_tables},n_projections: {self.n_projections}"
   