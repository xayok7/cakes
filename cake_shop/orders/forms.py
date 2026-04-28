from django import forms
from .models import Cake, Order


class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['base', 'cream', 'filling', 'decorations', 'size', 'shape']
        widgets = {
            'decorations': forms.CheckboxSelectMultiple()
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_type', 'address']