"""Script para criar superusuário e dados de exemplo para o blog."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post, Comment
from django.utils.text import slugify

# Superusuário admin
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@blogdjango.com',
        password='admin123',
        first_name='Administrador',
        last_name='Blog'
    )
    print('✅ Superusuário criado: admin / admin123')
else:
    admin = User.objects.get(username='admin')
    print('ℹ️  Superusuário admin já existe.')

# Usuário de exemplo
if not User.objects.filter(username='joao').exists():
    joao = User.objects.create_user(
        username='joao',
        email='joao@exemplo.com',
        password='senha123',
        first_name='João',
        last_name='Silva'
    )
    print('✅ Usuário criado: joao / senha123')
else:
    joao = User.objects.get(username='joao')

# Categorias
cats = [
    ('Tecnologia', 'tecnologia', 'Posts sobre programação e tecnologia'),
    ('Viagens', 'viagens', 'Dicas e experiências de viagem'),
    ('Culinária', 'culinaria', 'Receitas e dicas gastronômicas'),
]
cat_objs = {}
for name, slug, desc in cats:
    cat, created = Category.objects.get_or_create(
        slug=slug,
        defaults={'name': name, 'description': desc}
    )
    cat_objs[slug] = cat
    if created:
        print(f'✅ Categoria criada: {name}')

# Posts de exemplo
posts_data = [
    {
        'title': 'Introdução ao Django Framework',
        'content': '''Django é um framework web Python de alto nível que incentiva o desenvolvimento rápido e limpo.

Criado em 2003, Django foi desenvolvido por uma equipe de jornalistas para gerenciar sites de notícias com alto tráfego. Hoje é usado por grandes empresas como Instagram, Pinterest e Disqus.

**Principais características:**

- Arquitetura MTV (Model-Template-View)
- ORM poderoso para banco de dados
- Sistema de autenticação embutido
- Interface administrativa automática
- Sistema de templates robusto

Django segue o princípio "batteries included" - traz tudo que você precisa para criar uma aplicação web completa sem precisar de pacotes externos.

Neste blog, o projeto foi desenvolvido utilizando Django com três modelos relacionados: Category, Post e Comment, todos integrados com o User model nativo do Django.''',
        'category': 'tecnologia',
        'author': admin,
    },
    {
        'title': 'Por que Python é a linguagem do momento?',
        'content': '''Python se tornou a linguagem de programação mais popular do mundo, e não é à toa.

Sua sintaxe clara e legível permite que desenvolvedores sejam produtivos desde o primeiro dia. Além disso, o ecossistema de bibliotecas é imenso.

**Áreas onde Python brilha:**

1. Desenvolvimento Web (Django, Flask, FastAPI)
2. Data Science e Machine Learning (pandas, scikit-learn, TensorFlow)
3. Automação e Scripts
4. APIs e Microsserviços

A comunidade Python é acolhedora e os recursos de aprendizagem são abundantes e gratuitos.

Se você está começando na programação, Python é definitivamente a escolha certa para iniciar sua jornada!''',
        'category': 'tecnologia',
        'author': joao,
    },
    {
        'title': 'Dicas para viajar pela Europa com pouco dinheiro',
        'content': '''Viajar pela Europa não precisa custar uma fortuna! Com planejamento e algumas dicas, é possível conhecer o velho mundo sem quebrar o banco.

**Transporte:**
- Aproveite o Interrail Pass para trens ilimitados
- Use companhias aéreas low-cost como Ryanair e EasyJet
- Blablacar para caronas entre cidades

**Hospedagem:**
- Hostels são ótimos para quem viaja solo
- Airbnb pode sair mais barato para grupos
- Couchsurfing para a experiência mais autêntica

**Alimentação:**
- Faça compras no supermercado para café da manhã
- Piqueniques nos parques são econômicos e deliciosos
- Almoce nos mercados locais - mais barato que os restaurantes turísticos

Com essas dicas, dá para explorar a Europa inteira com um orçamento bem enxuto!''',
        'category': 'viagens',
        'author': admin,
    },
]

for data in posts_data:
    slug = slugify(data['title'])
    if not Post.objects.filter(slug=slug).exists():
        post = Post.objects.create(
            title=data['title'],
            slug=slug,
            content=data['content'],
            category=cat_objs[data['category']],
            author=data['author'],
            published=True,
        )
        print(f'✅ Post criado: {post.title}')

# Comentários de exemplo
first_post = Post.objects.first()
if first_post and not Comment.objects.filter(post=first_post).exists():
    Comment.objects.create(
        post=first_post,
        author=joao,
        content='Excelente post! Django é realmente incrível para desenvolvimento web rápido.'
    )
    Comment.objects.create(
        post=first_post,
        author=admin,
        content='Obrigado pelo comentário! Se tiver dúvidas, pode perguntar aqui nos comentários.'
    )
    print('✅ Comentários de exemplo criados.')

print('\n🎉 Setup concluído! Acesse http://localhost:8000 para ver o blog.')
print('   Admin: http://localhost:8000/admin — usuário: admin / senha: admin123')

