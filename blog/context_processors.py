from .models import Category


def nav_categories(request):
    """Injeta categorias em todos os templates para a navbar e footer."""
    return {
        'nav_categories': Category.objects.all()[:6]
    }

