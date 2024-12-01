from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Customer, ProductRating

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        help_text=''
    )

    class Meta:
        model = CustomUser  # Use the custom user model
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password2': None,
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_image', 'contact_no', 'barangay', 'street', 'city', 'province', 'zip_code']

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }
