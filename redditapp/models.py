# Required library for Django model definition
from django.db import models

# Defining the Post model.
class Post(models.Model):
    # Field for storing the post's title. The TextField is used for longer form text.
    title = models.TextField()

    # Field for storing the content of the post. The TextField is used here as posts can be long.
    content = models.TextField()

    # DateTimeField records the date and time a post was created. This can be used to sort posts chronologically.
    date_posted = models.DateTimeField()

    # String representation of the Post object. It returns the post's title to make it recognizable in the Django admin or any print statement.
    def __str__(self):
        return self.title

# Defining the Suggestion model.
class Suggestion(models.Model):
    # Field for storing the suggestion text. The TextField is used for longer form text.
    # The 'verbose_name' parameter is used to provide a more human-readable name in the Django admin.
    text = models.TextField(verbose_name="Suggestion Text")

    # DateTimeField records the date and time a suggestion was created. 'auto_now_add=True' sets the date/time when a record is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the Suggestion object. It returns the first 50 characters of the suggestion text to make it recognizable in the Django admin or any print statement.
    def __str__(self):
        return self.text[:50]  # Limiting the string representation to the first 50 characters for readability.
