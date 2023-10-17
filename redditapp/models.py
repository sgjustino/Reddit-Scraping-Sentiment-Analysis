from django.db import models

# Defining Post model.
class Post(models.Model):
    title = models.TextField()

    content = models.TextField()

    date_posted = models.DateTimeField()

    def __str__(self):
        return self.title

# Defining Suggestion model/Feedback.
class Suggestion(models.Model):
    text = models.TextField(verbose_name="Suggestion Text")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
