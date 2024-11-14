from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import User, Song

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'artist_image', 'album', 'cover_image', 'audio_file']

class UserDetailUpdateForm(UserChangeForm):
    password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter new password'}),
        required=False
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm new password'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Pop 'request' from kwargs if present
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = 'Leave blank if you do not want to change your password.'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)
            if commit:
                user.save()
                if self.request:
                    update_session_auth_hash(self.request, user)  # Update session auth hash

        return user
