from django import forms
from .models import Suggestion

#ModelForm to create forms directly from models.
class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['text']