from django import forms

from .models import Post, Comment, Profile

class PostForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'rows': '1', 'placeholder': 'Diga o que esta pensando...', 'background': 'black',}))

    image = forms.ImageField(required=False, widget=forms.FileInput())

    class Meta:
        model = Post
        fields = ['body', 'image']



class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.TextInput(
        attrs={'rows': '2', 'placeholder': 'Escreve uma mensagem...', 'background': 'black', 'focus:background': 'red', 'width': '30px',}
    ))

    class Meta:
        model = Comment
        fields = ['comment']