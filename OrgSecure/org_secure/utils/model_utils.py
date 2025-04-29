import cv2
import numpy as np
from typing import List, Dict, Any, Tuple


def split_face_embedding(data: List[Dict[str, Any]]) -> Tuple[List[np.ndarray], List[Dict[str, Any]]]:
    '''
    Separate facial area from embedding vector 
    '''
    embedding_vectors = []
    facial_areas = []
    
    for item in data:
        # Convert the embedding list to a NumPy array
        embedding_vectors.append(np.array(item.get('embedding', [])))
        facial_areas.append(item.get('facial_area', {}))        
    return embedding_vectors, facial_areas


def edite_image(image ,image_facial_area , name ):
    x, y, w, h = (image_facial_area['x'], image_facial_area['y'], image_facial_area['w'],image_facial_area['h'])
    # Draw a rectangle around the face
    cv2.rectangle(image, (x, y), (x + w, y + h), (255 , 0 , 0), 2)
    cv2.putText(image, f'{name}', (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255 , 0 , 0), 1)
    return image 


