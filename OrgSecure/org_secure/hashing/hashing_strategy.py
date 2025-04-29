import numpy as np
from typing import List
from abc import ABC , abstractmethod
class HashingStrategy(ABC):
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
    def get_model(self):
        pass