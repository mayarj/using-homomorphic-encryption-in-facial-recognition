import heapq
import numpy as np

class MinHeap:
    def __init__(self):
        self.heap = []

    def add(self, distance, index):
        # Push the distance to create a min-heap
        heapq.heappush(self.heap, (distance, index))
        
    def get_heap(self):
        # Return the heap contents as (distance, index)
        return self.heap  # No need to negate distances

    def get_indexes(self):
        return [index for distance, index in self.heap]

    def get_dis(self):
        return [distance for distance, index in self.heap]

    def get_smallest(self):
        """
        Return the distance and index for the smallest distance in the heap.
        If the heap is empty, return None.
        """
        if not self.heap:
            return None  # Return None if the heap is empty
        # The smallest distance will be the root of the min-heap
        smallest_distance, index = self.heap[0]
        return smallest_distance, index
    
    def return_k_rank(self , k:int ):
        return self.heap[:k]