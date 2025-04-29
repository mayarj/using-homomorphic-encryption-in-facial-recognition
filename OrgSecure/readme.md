# OrgSecure - Secure Biometric Authentication System

## Overview

OrgSecure is a Django-based application that provides secure biometric authentication using facial recognition, homomorphic encryption, and locality-sensitive hashing (LSH). The system allows organizations to securely store and query facial embeddings while preserving privacy through advanced cryptographic techniques.

## Key Features

- **Facial Recognition**: Uses DeepFace with Facenet model for accurate face embedding generation
- **Homomorphic Encryption**: Supports both CKKS (approximate) and BFV (exact) encryption schemes
- **Privacy-Preserving Matching**: Implements LSH for efficient and secure nearest neighbor search
- **Secure API Communication**: Encrypted data transmission between client and server
- **Modular Design**: Strategy pattern implementation for easy algorithm swapping

## Components

### Core Modules

1. **Encryption**
   - `EncryptionStrategy`: Abstract base class for encryption implementations
   - `CKKSStrategy`: Approximate homomorphic encryption implementation
   - `BFVStrategy`: Exact homomorphic encryption implementation

2. **Hashing**
   - `HashingStrategy`: Abstract base class for hashing implementations
   - `LSHStrategy`: Locality-Sensitive Hashing implementation

3. **Creators**
   - Factory pattern implementations for creating encryption and hashing strategies

4. **API Client**
   - Handles secure communication with the biometric service
   - Manages authentication tokens and encrypted data transmission

5. **Management Command**
   - `initialize_dataset.py`: Command to process and encrypt facial images

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/OrgSecure.git
   cd OrgSecure
   ```

3. Set up environment variables:
   - Create a `.env` file based on `.env.example`
   - Configure encryption parameters, API URLs, and credentials

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

## Configuration

Edit the `settings.py` file or environment variables to configure:

- Encryption parameters (CKKS/BFV)
- Hashing parameters (LSH dimensions/tables)
- Model settings (Facenet)
- API endpoints
- Storage locations for keys and hashes

## Usage

### Initializing the Dataset

To process facial images and initialize the encrypted database:
```bash
python manage.py initialize_dataset
```
note the server side should be running  

### Running the Application

Start the development server:
```bash
python manage.py runserver
```

Access the web interface at `http://localhost:8000`

### API Endpoints
- `/process-image/`: Submit an image for face recognition
- (Other endpoints are used internally by the system)

## Dependencies

- Django
- DeepFace
- TenSEAL (for homomorphic encryption)
- NumPy
- OpenCV
- Requests

## Security Considerations

- Always keep encryption keys secure
- Use HTTPS in production environments
- Regularly rotate authentication tokens
- Monitor system access and usage
