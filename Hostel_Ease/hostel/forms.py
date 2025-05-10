from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Application, Hostel, District

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user

class WardenRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'warden'
        user.is_approved = False  # Optional: Needs admin approval
        if commit:
            user.save()
        return user
    
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = []  # No fields needed; student and hostel are set in view

class HostelRegistrationForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'district', 'location', 'contact_email', 'phone_number', 'available_rooms', 'total_rooms', 'price_per_month', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
        }