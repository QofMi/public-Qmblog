from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Create ur form heere
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'user', 'img']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),

            'body': CKEditorUploadingWidget(),

        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()

            if new_slug == 'create':
                raise ValidationError('ERROR')
            return new_slug
