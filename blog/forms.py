from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')
    first_name = forms.CharField(max_length=50, required=True, label='Nome')
    last_name = forms.CharField(max_length=50, required=True, label='Sobrenome')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'category', 'content', 'image_url', 'featured', 'published')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Gaules bate recorde na Twitch...'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'placeholder': 'Escreva o conteúdo do artigo...'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'image_url': 'URL da Imagem de Capa (opcional)',
            'featured': 'Destacar na Home',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 3,
                'placeholder': 'O que você acha? Compartilhe sua opinião...',
            }),
        }
        labels = {'content': ''}
