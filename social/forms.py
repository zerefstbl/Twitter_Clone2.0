from django import forms

from .models import Post, Comment, Profile

class PostForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': '1', 'placeholder': 'Diga o que esta pensando...'}))

    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['body', 'image']
