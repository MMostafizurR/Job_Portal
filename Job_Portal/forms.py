from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Job

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    display_name = forms.CharField(max_length=100, required=True, label="Display Name")
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES, required=True, label="I am a")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {'username': '',}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class UserProfileForm(forms.ModelForm):

  class Meta:
    model = UserProfile
    fields = [
        'profile_picture',
        'display_name',
        'phone_number',
        'location',
        'website',
        'bio',
        'company_info',
        'skills_set',
        'resume',
    ]
    widgets = {
        'profile_picture': forms.ClearableFileInput(
            attrs={'class': 'form-control'}
        ),
        'display_name': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Full Name'}
        ),
        'phone_number': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': ''}
        ),
        'location': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': ''}
        ),
        'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': ''}),

    
        'bio': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '',
            }
        ),
        'company_info': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '',
            }
        ),
        'skills_set': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Python, Django, SQL...',
            }
        ),
        'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    }

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'number_of_openings', 'category', 'job_description', 'skills_set']
        widgets = {
            'job_description': forms.Textarea(attrs={'rows': 4}),
        }