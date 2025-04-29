from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    """
    Model to store additional profile information for users.
    Each user has a unique profile with preferences for hashing and encryption types.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hashing_type = models.CharField(max_length=50)  # Type of hashing strategy to use
    encryption_type = models.CharField(max_length=50) # Type of encryption strategy to use


    def __str__(self):
        """
        String representation of the UserProfile model.
        """
        return f"{self.user.username}'s Profile"


class EncryptedEmbedding(models.Model):
    """
    Model to store encrypted embeddings for users.
    Each embedding is associated with a user and an identification number.
    """
    embedding = models.JSONField()  # Store the encrypted embedding as JSON
    user = models.ForeignKey(User, on_delete=models.CASCADE ,default=0) # Associated user
    identification  = models.IntegerField(null=False, blank=False ,db_index= True ,default=0) #  identifier for the embedding

    class Meta:
        """
        Meta options for the EncryptedEmbedding model.
        """
        indexes = [
            models.Index(fields=['user', 'identification']),
        ]


    def save_encrypted(self, encrypted_data ,identification:int  , user:User):
        """
        Save an encrypted embedding to the database.

        Args:
            encrypted_data: The encrypted embedding to store.
            identification: identifier for the embedding.
            user: The user associated with the embedding.
        """
        self.embedding = encrypted_data
        self.identification = identification
        self.user = user
        self.save()

    def get_encrypted_embedding(self):
        """
        Retrieve the encrypted embedding.

        Returns:
            The encrypted embedding stored in the JSONField.
        """
        return self.embedding