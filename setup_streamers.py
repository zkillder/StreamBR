"""Script para alimentar o blog com o tema Streamers Brasileiros e imagens públicas"""
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
        email='admin@streambr.com',
        password='admin123',
        first_name='Admin',
        last_name='StreamBR'
    )
    print('✅ Superusuário criado: admin / admin123')
else:
    admin = User.objects.get(username='admin')

# Usuário streamer convidado
if not User.objects.filter(username='coringa_fan').exists():
    fan = User.objects.create_user(
        username='coringa_fan',
        email='fan@streambr.com',
        password='senha123',
        first_name='Lucas',
        last_name='Menezes'
    )
    print('✅ Usuário comum criado: coringa_fan / senha123')
else:
    fan = User.objects.get(username='coringa_fan')

# Categorias voltadas para streamers brasileiros
categories_data = [
    ('Tribo & CS', 'tribo-cs', 'Coberturas, Majors e o ecossistema liderado por Gaules e a Tribo.', 'bi-headset'),
    ('CazéTV & Esportes', 'cazetv-esportes', 'Transmissões esportivas, Copa do Mundo e o império de Casimiro Miguel.', 'bi-tv'),
    ('GTA RP & LOUD', 'gta-rp-loud', 'Histórias de Cidade Alta, Coringa, Paulinho o Loko e streamers da LOUD.', 'bi-controller'),
    ('Just Chatting & Humor', 'just-chatting', 'Podcasts ao vivo, bate-papos, react e momentos virais do streaming BR.', 'bi-chat-dots'),
    ('Eventos & Prêmios', 'eventos-premios', 'Prêmio eSports Brasil, CCXP, BGS e torneios beneficentes.', 'bi-trophy'),
]

cat_objs = {}
for name, slug, desc, icon in categories_data:
    cat, _ = Category.objects.get_or_create(
        slug=slug,
        defaults={'name': name, 'description': desc, 'icon': icon}
    )
    cat.icon = icon
    cat.description = desc
    cat.save()
    cat_objs[slug] = cat

# Posts com dados reais/temáticos e imagens públicas de streaming/esports
posts_data = [
    {
        'title': 'O Fenômeno Casimiro: Da Twitch para a Quebra de Recordes Mundiais no YouTube com a CazéTV',
        'category': 'cazetv-esportes',
        'author': admin,
        'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1200&q=80',
        'featured': True,
        'content': """Casimiro Miguel se consolidou como uma das maiores forças da história do entretenimento e streaming mundial. 

O que começou como lives descontraídas nas madrugadas da Twitch comentando vídeos de comida e construções no canal 'Cortes do Casimiro' rapidamente se transformou em uma revolução midiática. Com a criação da CazéTV em parceria com a LiveMode, Casimiro adquiriu os direitos e transmitiu a Copa do Mundo FIFA 2022, quebrando o recorde de live mais assistida do YouTube mundial com mais de 6 milhões de dispositivos simultâneos no jogo do Brasil contra a Croácia.

O estilo autêntico, sem o engessamento da televisão tradicional e com linguagem próxima do jovem, abriu caminho para a transmissão de Olimpíadas, Brasileirão e Copa Sul-Americana, mudando para sempre como o brasileiro consome esportes ao vivo na internet."""
    },
    {
        'title': 'Gaules e a Força da Tribo: Como a Paixão pelo CS Moldou a Cultura Gamer no Brasil',
        'category': 'tribo-cs',
        'author': admin,
        'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80',
        'featured': True,
        'content': """Alexandre 'Gaules' Borba não é apenas um dos maiores streamers do mundo, mas também um símbolo de superação e perseverança. Ex-jogador e ex-treinador profissional de Counter-Strike na era de ouro da mibr em 2006, Gaules encontrou na transmissão de torneios uma salvação pessoal e profissional.

Com seu famoso lema "A Tribo cuida da Tribo", ele transformou o canal num ponto de encontro acolhedor. Em 2022, durante o Major da Antuérpia, Gaules alcançou mais de 710 mil espectadores simultâneos na Twitch acompanhando o confronto da Imperial de Fallen. 

Além dos recordes de audiência, Gaules é pioneiro em adquirir direitos esportivos na Twitch brasileira, trazendo transmissões da NBA, F1 e criando um ecossistema com podcast, torneios comunitários e causas sociais."""
    },
    {
        'title': 'O Fenômeno do GTA RP: Coringa, Paulinho o Loko e as Narrativas que Pararam o Brasil',
        'category': 'gta-rp-loud',
        'author': fan,
        'image_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=1200&q=80',
        'featured': True,
        'content': """Nos últimos anos, o Brasil tornou-se a capital indiscutível do Grand Theft Auto Roleplay (GTA RP). Servidores como Cidade Alta e Complexo viraram verdadeiras novelas em tempo real onde criadores interpretam personagens marcantes todos os dias.

Victor 'Coringa' Augusto, streamer da LOUD, se consolidou nas transmissões diárias com audiências gigantescas, mesclando comédia, ação policial e dramas comunitários no servidor. 

Paralelamente, Alisson 'Paulinho o Loko' atingiu números astronômicos com seu humor irreverente e improviso rápido, tornando o GTA RP uma das categorias mais vistas no país inteiro, rivalizando diretamente com gigantes internacionais."""
    },
    {
        'title': 'Alanzoka e o Legado da Variedade: Carisma Constante e Comunidade Fiel',
        'category': 'just-chatting',
        'author': fan,
        'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80',
        'featured': False,
        'content': """Alan 'Alanzoka' Ferreira é um dos pioneiros absolutos da criação de conteúdo gamer no Brasil. Vindo da época do YouTube raiz com jogos de terror independentes, ele migrou com maestria para a Twitch, mantendo uma legião de fãs há mais de uma década.

Ao contrário de muitos streamers focados em um único jogo competitivo, Alan é o rei das 'gameplays de variedade': lançamentos AAA, indies desconhecidos, jogos de suspense e cooperativos. 

Sua live é famosa pela ausência de toxicidade e pela risada contagiante, provando que longevidade na internet se constrói com carisma sincero e respeito à comunidade."""
    },
    {
        'title': 'Prêmio eSports Brasil e Streamers Awards: A Profissionalização da Indústria Nacional',
        'category': 'eventos-premios',
        'author': admin,
        'image_url': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=80',
        'featured': False,
        'content': """O mercado brasileiro de streaming amadureceu a ponto de movimentar milhões de reais em patrocínios de marcas multinacionais como Itaú, Nike, Red Bull e Ambev. 

Eventos anuais de premiação consagram criadores em categorias como 'Melhor Streamer', 'Personalidade do Ano' e 'Revelação'. O setor hoje envolve agências especializadas, produtoras audiovisuais de ponta e infraestruturas técnicas dignas das maiores emissoras de TV do país."""
    }
]

for p in posts_data:
    slug = slugify(p['title'])
    post, created = Post.objects.get_or_create(
        slug=slug,
        defaults={
            'title': p['title'],
            'content': p['content'],
            'author': p['author'],
            'category': cat_objs[p['category']],
            'image_url': p['image_url'],
            'featured': p['featured'],
            'published': True,
        }
    )
    if not created:
        post.image_url = p['image_url']
        post.featured = p['featured']
        post.content = p['content']
        post.category = cat_objs[p['category']]
        post.save()
    print(f'✅ Artigo: {post.title[:50]}...')

# Comentários
caze_post = Post.objects.filter(slug__contains='casimiro').first()
if caze_post:
    Comment.objects.get_or_create(
        post=caze_post,
        author=fan,
        defaults={'content': 'A live da Copa do Mundo foi histórica demais! Casimiro merece todo o sucesso do mundo.'}
    )
    Comment.objects.get_or_create(
        post=caze_post,
        author=admin,
        defaults={'content': 'Concordo plenamente! E a transmissão das Olimpíadas de Paris na CazéTV só consolidou isso.'}
    )

gau_post = Post.objects.filter(slug__contains='gaules').first()
if gau_post:
    Comment.objects.get_or_create(
        post=gau_post,
        author=fan,
        defaults={'content': 'A Tribo não é apenas um canal, é uma família! O Major da Antuérpia me marcou pra sempre.'}
    )

print('\n🎉 Dados sobre Streamers Brasileiros atualizados com sucesso!')

