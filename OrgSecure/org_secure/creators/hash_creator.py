from abc import ABC ,abstractmethod
import importlib
from ..hashing.hashing_strategy import HashingStrategy
from django.conf import settings


class HashingCreator(ABC):
    @abstractmethod
    def create(self) -> HashingStrategy:
        pass


class  HashingCreatorImpl( HashingCreator):
    hashing_strategy = None
    
    def create  (
                self,
                n_dimensions = settings.HASHING_PARAM['n_dimensions'],
                n_tables = settings.HASHING_PARAM['n_tables'],
                n_projections = settings.HASHING_PARAM['n_projections'],
                )->HashingStrategy:

        if HashingCreatorImpl.hashing_strategy is None :

            module_path, class_name = settings.HASHING_CLASSES[settings.HASHING_STRATEGY].rsplit('.', 1)
            module = importlib.import_module(module_path)
            strategy_class = getattr(module, class_name)
            hashing_strategy = strategy_class( 
                    n_dimensions = n_dimensions,
                    n_tables = n_tables,
                    n_projections = n_projections,
                )
            HashingCreatorImpl.hashing_strategy = hashing_strategy
        return  HashingCreatorImpl.hashing_strategy 
       