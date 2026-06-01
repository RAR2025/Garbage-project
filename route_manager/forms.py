from django import forms
from .models import Shop

class ShopWeightForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['garbage_weight']