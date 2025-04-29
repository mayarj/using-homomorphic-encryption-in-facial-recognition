import base64
import os 
def read_data(file_name):
    '''
    this function read encription key for some what fully homonorphic and fully homomorphic 
    '''
    if os.path.exists(file_name) :
        with open(file_name, 'rb') as f:
            file_content = f.read()

        return base64.b64decode(file_content) 
    return None


def write_data(file_name, file_content):
    '''
    this function writes encription key for some what fully homonorphic and fully homomorphic 
    '''

    file_content = base64.b64encode(file_content)
    
    with open(file_name, 'wb') as f:
        f.write(file_content)
