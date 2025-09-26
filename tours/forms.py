import re
from django import forms

class BookingForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Full name', 'class': 'form-input'}),
        error_messages={'required': 'Please enter your full name.'}
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'form-input'}),
        error_messages={'required': 'Please provide an email address.'}
    )
    attendees = forms.IntegerField(
        min_value=1,
        max_value=20,
        label="Number of Guests",
        widget=forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'max': '20'}),
        error_messages={
            'min_value': 'At least one guest is required.',
            'max_value': 'Please contact us for groups larger than 20.'
        }
    )

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '').strip()
        # allow letters, spaces, hyphens and apostrophes
        if not re.match(r"^[A-Za-z\s\'\-]+$", name):
            raise forms.ValidationError("Enter a valid name (letters, spaces, hyphens and apostrophes only).")
        return name
