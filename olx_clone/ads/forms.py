from django import forms
from .models import VehicleAd

class VehicleAdForm(forms.ModelForm):
    class Meta:
        model = VehicleAd
        fields = ['name', 'model', 'price', 'image']

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Enter your feedback', 'rows': 4, 'cols': 50}),
        }
