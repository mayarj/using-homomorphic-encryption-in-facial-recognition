import numpy as np 
from django.test import TestCase
from ..creators.hash_creator import HashingCreatorImpl
from ..hashing.lsh_strategy import LSHStrategy 





class TestHashing(TestCase):

    def setUp(self):
        """Set up the environment for the tests."""
        np.random.seed(42)
        self.creator = HashingCreatorImpl()
        self.n_dimensions = 10
        self.n_points = 16000
        self.points = [np.random.randn(self.n_dimensions) for _ in range(self.n_points)]
        self.lsh =  self.creator.create(n_dimensions= self.n_dimensions ,  ID=5 , hashing_type='LSH')
        self.assertIsInstance(self.lsh, LSHStrategy )
        

    def test_model_creation(self):
        """Test the creation of the LSH model."""
        print ( " lsh test creating ,  saving and   loading model ")
       
        ids = np.arange(self.n_points)
        self.lsh.Initialize()
        self.lsh.create_hashing(self.points , ids )
        self.lsh.save_model()
        lsh_loaded = self.creator.create( ID=5, hashing_type='LSH' )
        self.assertIsNotNone(lsh_loaded, "Loaded LSH model should not be None.")

    def test_query_point_hash(self):
        """Test the hashing of a query point."""
        print ( "Test the hashing of a query point.")
        lsh_loaded   =self.creator.create( ID=5, hashing_type='LSH' )
        query_point = np.random.randn(self.n_dimensions)
        query_hash = lsh_loaded.get_point_hash(query_point)
        self.assertIsNotNone(query_hash, "Query point hash should not be None.")
        print("Query point hash:", query_hash)

    def test_nearest_neighbors(self):
        """Test retrieving nearest neighbors."""
        print ( "Test retrieving nearest neighbors.")
        lsh_loaded   = self.creator.create( ID=5, hashing_type='LSH' )
        query_point = np.random.randn(self.n_dimensions)
        query_hash = lsh_loaded.get_point_hash(query_point)
        print ( "query_hash" ,len (query_hash ) )
        nearest_neighbors = lsh_loaded.get_k_nearest(query_hash)
        self.assertIsInstance(nearest_neighbors, list, "Nearest neighbors should be a list.")
        print(f"Number of nearest neighbors: {len(nearest_neighbors)}")

    def test_nearest_neighbors(self):
        lsh_loaded   = self.creator.create( ID=1, hashing_type='LSH' )
        print (lsh_loaded  )
