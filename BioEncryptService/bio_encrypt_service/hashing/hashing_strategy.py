import numpy as np
from typing import List
from abc import ABC , abstractmethod
class hashingStrategy(ABC):
    """
    Abstract base class for hashing strategies.
    Provides a common interface for hashing, indexing, and querying.
    Derived classes must implement the abstract methods.
    """
    @abstractmethod
    def __init__(   self,
                    ID : int  ,
                    n_dimensions: int ,
                    n_tables: int,
                    n_projections: int 
                ):
        """
        Initialize the hashing strategy.

        Args:
            ID (int): Unique identifier for the hashing model.
            n_dimensions (int): Number of dimensions of the data points.
            n_tables (int): Number of hash tables.
            n_projections (int): Number of random projections per hash table.
        """
        pass
    
    @abstractmethod
    def Initialize(self):
        """
        Initialize the hashing model (e.g., generate random projections).
        """
        pass

    @abstractmethod
    def hash_point(self, point: np.ndarray, projection: np.ndarray):
        """
        Compute the hash of a point using a given projection matrix.

        Args:
            point (np.ndarray): The point to hash (n-dimensional numpy array).
            projection (np.ndarray): The projection matrix.

        Returns:
            str: The hash as a string (e.g., "1010").
        """
        pass

    @abstractmethod
    def create_hashing(self, points: List[np.ndarray] , ids : np.ndarray):
        """
        Create the LSH index from a list of points.

        Args:
            points (List[np.ndarray]): List of n-dimensional points.
            ids (np.ndarray): List of IDs corresponding to the points.
        """
        pass

    @abstractmethod
    def update_hashing( self , point_hashs , id , final = False  ):
        """
        Update the Hashing index with a new point.

        Args:
            point_hashs: Hashes of the new point for each hash table.
            id: ID of the new point.
        """
        pass

    @abstractmethod
    def get_point_hash(self, point: np.ndarray) -> List[str]:
        """
        Compute the hash of a point using the LSH.

        Args:
            point (np.ndarray): The point to hash.

        Returns:
            List[str]: List of hashes (one for each hash table).
        """
        pass

    @abstractmethod
    def get_k_nearest(self, point_hash: List[str]):
        """
        Find the k-nearest neighbors of a point using its hash.

        Args:
            point_hash (List[str]): The hash of the query point.

        Returns:
            List of candidate IDs (nearest neighbors).
        """
        pass

    @abstractmethod
    def save_model(self):
        """
        Save the LSH model to disk.
        """
        pass

    @abstractmethod
    def load_model(self ):
        """
        Load the LSH model from disk.
        """
        pass

    @abstractmethod
    def receive_model(self , data):
        """
        Load the LSH model from serialized data.

        Args:
            data: Serialized LSH model data.
        """
        pass
   