from .models import Digit
from django import forms 

class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = Digit
        fields = ('image',)