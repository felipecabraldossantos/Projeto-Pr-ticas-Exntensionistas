from django.shortcuts import render, redirect
from .models import Produto
from django.shortcuts import get_object_or_404

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/home.html', {'produtos': produtos})

def estoque_view(request):
    query = request.GET.get('q')
    if query:
        produtos = Produto.objects.filter(descproduto__icontains=query)
    else:
        produtos = Produto.objects.all()
    return render(request, 'estoque/estoque.html', {'produtos': produtos})

def produto_view(request):
    # Pegando unidades distintas já existentes no banco
    unidades = Produto.objects.values_list('unidadedemedida', flat=True).distinct()

    if request.method == 'POST':
        desc = request.POST.get('descproduto')
        estoque = request.POST.get('estoqueproduto')
        unidade = request.POST.get('unidadedemedida')

        if desc and estoque and unidade:
            Produto.objects.create(
                descproduto=desc,
                estoqueproduto=estoque,
                unidadedemedida=unidade
            )
            return redirect('produto')

    produtos = Produto.objects.all()
    return render(request, 'estoque/produto.html', {'produtos': produtos, 'unidades': unidades})
    
def pedido_view(request):
    return render(request, 'estoque/pedido.html')

def editar_produto_view(request, produto_id):
    produto = get_object_or_404produto = get_object_or_404(Produto, idproduto=produto_id)
    unidades = Produto.objects.values_list('unidadedemedida', flat=True).distinct()

    if request.method == 'POST':
        produto.descproduto = request.POST.get('descproduto')
        produto.unidadedemedida = request.POST.get('unidadedemedida')
        produto.save()
        return redirect('produto')

    return render(request, 'estoque/editar_produto.html', {
        'produto': produto,
        'unidades': unidades
    })

def editar_produto_redirect_view(request):
    produto_id = request.GET.get("produto_id")
    if produto_id:
        return redirect('editar_produto', produto_id=produto_id)
    return redirect('produto')