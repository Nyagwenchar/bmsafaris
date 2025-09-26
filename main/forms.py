from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name (optional)',
                'aria-label': 'Your name',
                'class': (
                    'w-full p-3 rounded bg-black/40 border border-gray-400 text-white '
                    'placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-400'
                )
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your review...',
                'rows': 4,
                'aria-label': 'Review content',
                'maxlength': '300',   # ✅ moved inside attrs
                'required': 'true',   # ✅ proper HTML attribute
                'aria-required': 'true',
                'class': (
                    'w-full p-3 rounded bg-black/40 border border-gray-400 text-white '
                    'placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-400'
                )
            }),
        }
        error_messages = {
            'name': {
                'max_length': 'Name is too long.',
            },
            'content': {
                'required': 'This field is required.',
                'max_length': 'Too long — please keep it under 300 characters.',
            },
        }

    def clean_content(self):
        """Extra server-side validation to ensure 300 char max."""
        content = self.cleaned_data.get('content', '')
        if len(content) > 300:
            raise forms.ValidationError("Review cannot exceed 300 characters.")
        return content

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Tailwind error styling if the form is bound and has errors
        if self.is_bound:
            for bound_field in self.visible_fields():
                if bound_field.errors:
                    css = bound_field.field.widget.attrs.get("class", "")
                    if "border-red-500" not in css:
                        bound_field.field.widget.attrs["class"] = css + " border-red-500"
