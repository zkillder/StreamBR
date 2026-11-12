from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('categoria/<slug:slug>/', views.category_posts, name='category_posts'),

    # Autenticação
    path('cadastro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Ações restritas (login_required)
    path('novo-post/', views.post_create, name='post_create'),
    path('post/<slug:slug>/editar/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/excluir/', views.post_delete, name='post_delete'),
    path('meus-posts/', views.my_posts, name='my_posts'),
]

