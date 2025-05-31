from django import forms
from .models import Customer


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
    
class CustomerImageForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'mobile', 'address','image']
        
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'email', 'mobile', 'address']


