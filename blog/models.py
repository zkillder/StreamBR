from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """Categorias do blog de streamers"""
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descrição')
    icon = models.CharField(max_length=50, blank=True, default='bi-controller', verbose_name='Ícone Bootstrap')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """Posts/artigos sobre streamers brasileiros"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Autor'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Categoria'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    content = models.TextField(verbose_name='Conteúdo')
    # URL de imagem pública (Unsplash, etc.)
    image_url = models.URLField(
        blank=True,
        default='',
        verbose_name='URL da Imagem de Capa'
    )
    featured = models.BooleanField(default=False, verbose_name='Destaque')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    published = models.BooleanField(default=True, verbose_name='Publicado')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_image(self):
        """Retorna a imagem do post ou uma imagem padrão baseada no slug."""
        if self.image_url:
            return self.image_url
        return f'https://picsum.photos/seed/{self.slug}/800/450'


class Comment(models.Model):
    """Comentários nos posts — requer usuário logado"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Post'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Autor'
    )
    content = models.TextField(verbose_name='Comentário')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

    def __str__(self):
        return f'Comentário de {self.author.username} em "{self.post.title}"'
