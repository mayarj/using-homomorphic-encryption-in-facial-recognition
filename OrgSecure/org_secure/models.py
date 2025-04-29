from django.db import models

# Create your models here.

class Person(models.Model):
    # Unique constraint on first_name and last_name together
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def save_person(self, firstname, lastname):
        # Check if a person with the same first and last name already exists
        existing_person = Person.objects.filter(first_name=firstname, last_name=lastname).first()
        if existing_person:
            return existing_person  # Return the existing person
        
        # If not, create a new person
        self.first_name = firstname
        self.last_name = lastname
        self.save()
        return self
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
