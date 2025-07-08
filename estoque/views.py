from django.shortcuts import render
from .models import Produto

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/home.html', {'produtos': produtos})

def estoque_view(request):
    query = request.GET.get('q')  # Pega o que o usuário digitou
    if query:
        produtos = Produto.objects.filter(descproduto__icontains=query)
    else:
        produtos = Produto.objects.all()

    return render(request, 'estoque/estoque.html', {'produtos': produtos})

def produto_view(request):
    return render(request, 'estoque/produto.html')

def pedido_view(request):
    return render(request, 'estoque/pedido.html')
