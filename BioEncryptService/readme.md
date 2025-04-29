# Secure Face Processing and Retrieval System

This project implements a secure face processing and retrieval system using **homomorphic encryption** and **locality-sensitive hashing (LSH)**. It allows users to register, log in, and securely store and retrieve face embeddings while protecting biometric data.

---

## Features

- **User Authentication**:
  - Register and log in using JWT (JSON Web Tokens).
  - Secure password storage and validation.

- **Face Embedding Encryption**:
  - Encrypt face embeddings using **CKKS** or **BFV** homomorphic encryption schemes.
  - Perform operations (e.g., distance calculations) on encrypted data.

- **Locality-Sensitive Hashing (LSH)**:
  - Efficiently index and retrieve similar face embeddings using LSH.
  - Update and query the LSH index securely.

- **Middleware Integration**:
  - Attach encryption and hashing instances to authenticated requests.

- **RESTful API**:
  - Expose endpoints for user registration, login, face addition, and retrieval.

---

## Technologies Used

- **Backend**:
  - Django
  - Django REST Framework
  - SimpleJWT for authentication

- **Encryption**:
  - TenSEAL (CKKS and BFV schemes)

- **Hashing**:
  - Locality-Sensitive Hashing (LSH)

- **Database**:
  - SQLite (default), PostgreSQL (recommended for production)

- **Logging**:
  - Python's `logging` module

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- PostgreSQL (optional, for production)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/secure-face-retrieval.git
   cd secure-face-retrieval
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```


3. **Set up the database**:
   - For SQLite (default):
     ```bash
     python manage.py migrate
     ```
   - For PostgreSQL:
     - Update `DATABASES` in `settings.py`:
       ```python
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': 'your_db_name',
               'USER': 'your_db_user',
               'PASSWORD': 'your_db_password',
               'HOST': 'localhost',
               'PORT': '5432',
           }
       }
       ```
     - Run migrations:
       ```bash
       python manage.py migrate
       ```

4. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### **Authentication**
- **Register**:
  - `POST /api/register/`
  - Request Body:
    ```json
    {
      "username": "user123",
      "email": "user123@example.com",
      "password": "securepassword123",
      "hashing_type": "lsh",
      "encryption_type": "ckks"
    }
    ```
  - Response:
    ```json
    {
      "user_id": 1,
      "username": "user123",
      "email": "user123@example.com",
      "hashing_type": "lsh",
      "encryption_type": "ckks",
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

- **Login**:
  - `POST /api/login/`
  - Request Body:
    ```json
    {
      "username": "user123",
      "password": "securepassword123"
    }
    ```
  - Response:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "username": "user123",
      "email": "user123@example.com",
      "user_id": 1,
      "hashing_type": "lsh",
      "encryption_type": "ckks"
    }
    ```

### **Face Processing**
- **Add Face**:
  - `POST /api/add-face/`
  - Request Body:
    ```json
    {
      "encrypted_data": "base64_encoded_encrypted_embedding",
      "point_hash": "1010",
      "point_identification": 123
    }
    ```
  - Response:
    ```json
    {
      "message": "Face added successfully."
    }
    ```

- **Retrieve Nearest Neighbors**:
  - `GET /api/knerast/`
  - Request Body:
    ```json
    {
      "encrypted_data": "base64_encoded_encrypted_embedding",
      "point_hash": "1010"
    }
    ```
  - Response:
    ```json
    {
      "iden_distance": {
        "123": "base64_encoded_distance",
        "456": "base64_encoded_distance"
      }
    }
    ```

---

## Configuration

### Environment Variables
- Create a `.env` file in the project root:
  ```env
  SECRET_KEY=your_django_secret_key
  DEBUG=True
  DATABASE_URL=postgres://user:password@localhost:5432/dbname
  ```

### Encryption and Hashing
- Update `ENCRYPTION_CLASSES` and `HASHING_CLASSES` in `config.py` to add or modify encryption/hashing strategies.

---

## Logging

Logs are stored in `logs/secure_face_retrieval.log`. Use the following log levels:
- `INFO`: General operations (e.g., user registration, face addition).
- `WARNING`: Non-critical issues (e.g., invalid input).
- `ERROR`: Critical errors (e.g., database failures).


---

## Acknowledgments

- [TenSEAL](https://github.com/OpenMined/TenSEAL) for homomorphic encryption.
- [Django REST Framework](https://www.django-rest-framework.org/) for building the API.
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) for JWT authentication.

---
