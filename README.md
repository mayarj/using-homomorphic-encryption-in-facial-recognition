# Secure Biometric Authentication Client

## Project Overview

This project is the client-side component of a secure biometric authentication system that works in conjunction with the [Secure Face Processing and Retrieval System]. Together, they form a complete solution for privacy-preserving facial recognition.

## Key Idea

The system provides:
- Secure facial embedding storage using homomorphic encryption (CKKS/BFV)
- Efficient similarity search through Locality-Sensitive Hashing (LSH)
- Privacy-preserving biometric authentication
- Secure communication between client and server

The client (OrgSecure) handles:
- Face image processing and embedding generation
- Local encryption of biometric data
- Secure API communication with the server
- Management of encryption keys and hashing parameters

the server (BioEncryptService) handels:
-  Encrypted Biometric Storage
-  Secure Matching Operations
-  Key Management

## Important Notes

1. **Testing Considerations**:
   - When running tests on the server side , the `assets/` directory should be deleted afterword to ensure clean test environments
   - This includes encryption keys and hashing models

2. **Security Note**:
   - If you change user credentials claint side  in the configuration:
     ```bash
     rm -rf assets/
     ```
   - This ensures no stale cryptographic material remains that might be tied to old credentials

## For Full Documentation

Please refer to the complete readme file  for:
- Detailed setup instructions
- API documentation
- Configuration options
- Usage examples

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt


cd .\BioEncryptService\
# create the database
ython manage.py migrate

# run the server side
python manage.py runserver
```
```bash
cd .\OrgSecure\

# create the database
ython manage.py migrate

# Initialize the system (creates assets/ directory) on the client side
python manage.py initialize_dataset

# Run the development server
python manage.py runserver <IP Addres >  # run on a defrant IP Address then the server 
```

