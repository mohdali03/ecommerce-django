# forms.py
from django import forms
from .models import Orders

class CheckoutForm(forms.ModelForm):
    # We add two extra address fields and two hidden fields
    address1 = forms.CharField(
        label="Address Line 1", 
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St', 'class': 'form-control'})
    )
    address2 = forms.CharField(
        label="Address Line 2", 
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor', 'class': 'form-control'})
    )
    amount = forms.IntegerField(
        label="Amount (INR)", 
        widget=forms.HiddenInput()
    )
    items_json = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = Orders
        # Exclude 'address' since we build it from address1 and address2.
        fields = ['name', 'email', 'phone', 'city', 'state', 'zip_code', 'items_json', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        address1 = cleaned_data.get('address1', '')
        address2 = cleaned_data.get('address2', '')
        # Combine the two address fields into one
        cleaned_data['address'] = f"{address1} {address2}"
        return cleaned_data
