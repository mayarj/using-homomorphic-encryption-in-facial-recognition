import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserProfile
from .creators.encryption_creator import EncryptionCreatorImpl
from .creators.hash_creator import HashingCreatorImpl
from .serializers import User

logger = logging.getLogger('bio_encrypt_service')
class ClassMiddleware:
    """
    Middleware to initialize and attach encryption and hashing instances to the request object.
    These instances are created based on the authenticated user's profile settings.
    """
    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response: The next middleware or view in the Django request/response chain.
        """
        self.hashing_creator =  HashingCreatorImpl()  # Factory for creating hashing strategies
        self.encryption_crator = EncryptionCreatorImpl() # Factory for creating encryption strategies
        self.get_response = get_response  # Store the next middleware or view
        self.CkksInstances = {}   # Dictionary to store encryption instances per user
        self.LshInstances = {} # Dictionary to store hashing instances per user
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        """
        Process the request and attach encryption/hashing instances to the request object.

        Args:
            request: The Django request object.

        Returns:
            HttpResponse: The response from the next middleware or view.
        """
        # Log the initial state of request.user
        logger.debug(f"Initial request.user: {request.user}")

        # Extract the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION' , None )

        logger.debug(f"Authorization header: {auth_header}")

        # Try to authenticate the user using the JWT token
        user = request.user
        if auth_header and auth_header.startswith('Bearer '):
            try:
                validated_token = self.jwt_authentication.get_validated_token(auth_header.split(' ')[1])
                user = self.jwt_authentication.get_user(validated_token)
                request.user = user  # Set the user on the request
                logger.debug(f"Authenticated user: {user}")
            except Exception as e:
                logger.warning(f"JWT Authentication failed: {e}")
                request.user = None # Ensure user is none if authentication fails.
        else:
            logger.debug("No Bearer token found")
        if user.is_authenticated:
            # Fetch the user's profile to get encryption and hashing preferences
            user_profile = UserProfile.objects.get(user=user)
            # Initialize instances if not already done
            if user.id not in self.CkksInstances :
                # Create encryption instance using the factorie
                self.CkksInstances[user.id] = self.encryption_crator.create(user.id , user_profile.encryption_type)
            if user.id not in self.LshInstances :
                # Create hashing instance using the factorie
                self.LshInstances[user.id] = self.hashing_creator.create(user.id , user_profile.hashing_type)
            # Attach instances to the request
            request.CkksInstance = self.CkksInstances[user.id]
            request.LshInstance = self.LshInstances[user.id]

        else:
            # Clear instances for unauthenticated users
            request.CkksInstance = None
            request.LshInstance = None
        
        # Call the next middleware or view in the chain
        response = self.get_response(request)
        return response
