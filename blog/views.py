from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.text import slugify
from .models import Post, Comment, Category
from .forms import RegisterForm, PostForm, CommentForm


# ---------- PÁGINAS PÚBLICAS ----------

def home(request):
    """Página inicial com posts em destaque e recentes"""
    featured_posts = Post.objects.filter(published=True, featured=True).select_related('author', 'category')[:3]
    recent_posts = Post.objects.filter(published=True).select_related('author', 'category')[:9]
    categories = Category.objects.all()
    total_posts = Post.objects.filter(published=True).count()
    total_comments = Comment.objects.count()
    return render(request, 'blog/home.html', {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'total_posts': total_posts,
        'total_comments': total_comments,
    })


def post_detail(request, slug):
    """Detalhe de um post e formulário de comentário (login obrigatório para comentar)"""
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.select_related('author')
    related_posts = Post.objects.filter(
        published=True, category=post.category
    ).exclude(id=post.id).select_related('author')[:3]
    form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Você precisa estar logado para comentar.')
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comentário publicado!')
            return redirect('post_detail', slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'related_posts': related_posts,
    })


def category_posts(request, slug):
    """Lista posts por categoria"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, published=True).select_related('author')
    categories = Category.objects.all()
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts,
        'categories': categories,
    })


# ---------- AUTENTICAÇÃO ----------

def register_view(request):
    """Cadastro de novo usuário"""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bem-vindo(a) à comunidade, {user.first_name}! 🎮')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    """Login de usuário"""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'De volta ao chat, {user.first_name or user.username}! 🔴 LIVE')
            return redirect('home')
    else:
        form = AuthenticationForm()
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control bg-dark text-light border-secondary'
    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):
    """Logout do usuário"""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Você saiu. Até a próxima live! 👋')
    return redirect('home')


# ---------- AÇÕES RESTRITAS (login_required) ----------

@login_required
def post_create(request):
    """Criação de artigo — somente usuários logados"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if not post.slug:
                post.slug = slugify(post.title)
            post.save()
            messages.success(request, '🎉 Artigo publicado com sucesso!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Publicar'})


@login_required
def post_edit(request, slug):
    """Edição de artigo — somente o autor ou staff"""
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, '⛔ Você não tem permissão para editar este artigo.')
        return redirect('post_detail', slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Artigo atualizado com sucesso!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Atualizar', 'post': post})


@login_required
def post_delete(request, slug):
    """Exclusão de artigo — somente o autor ou staff"""
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, '⛔ Você não tem permissão para excluir este artigo.')
        return redirect('post_detail', slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '🗑️ Artigo excluído.')
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def my_posts(request):
    """Lista artigos do usuário logado"""
    posts = Post.objects.filter(author=request.user).select_related('category')
    return render(request, 'blog/my_posts.html', {'posts': posts})
