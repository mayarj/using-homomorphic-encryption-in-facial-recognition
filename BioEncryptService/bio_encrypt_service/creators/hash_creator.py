from abc import ABC ,abstractmethod
import importlib
from ..hashing.hashing_strategy import hashingStrategy
from django.conf import settings


class HashingCreator(ABC):
    @abstractmethod
    def create(self) -> hashingStrategy:
        pass


class  HashingCreatorImpl( HashingCreator):
    

    def create  (
                self,
                ID:int ,
                n_dimensions = settings.HASHING_PARAM['n_dimensions'],
                n_tables = settings.HASHING_PARAM['n_tables'],
                n_projections = settings.HASHING_PARAM['n_projections'],
                hashing_type: str = "LSH" 
                )->hashingStrategy:
        


        if hashing_type in settings.HASHING_CLASSES.keys():

            module_path, class_name = settings.HASHING_CLASSES[hashing_type].rsplit('.', 1)
            module = importlib.import_module(module_path)
            strategy_class = getattr(module, class_name)
            hashing_strategy = strategy_class( 
                    n_dimensions = n_dimensions,
                    n_tables = n_tables,
                    n_projections = n_projections,
                    ID = ID
                )
            return  hashing_strategy
        else:
            raise ValueError(f"Unknown encryption type: {hashing_type}")