from django.shortcuts import render, redirect
from .models import Produto, Pedido
from django.shortcuts import get_object_or_404
from django.utils import timezone

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

def pedido_view(request):
    produtos = Produto.objects.all()
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    # Selecionar pedido
    if request.method == 'POST' and 'selecionar_pedido' in request.POST:
        pedido_id = request.POST.get('pedido_selecionado')
        if pedido_id:
            return redirect('editar_pedido', pedido_id=pedido_id)

    # Cadastrar novo pedido
    if request.method == 'POST' and 'cadastrar_pedido' in request.POST:
        nome = request.POST.get('nomepedido')
        desc = request.POST.get('descpedido')
        qtd = request.POST.get('qtdpedido')
        status = request.POST.get('statuspedido')
        datainicio = request.POST.get('datainicio')
        datafim = request.POST.get('datafim')
        produto_id = request.POST.get('produto')
        tipo = request.POST.get('tipopedido')

        if nome and qtd and status and datainicio and produto_id and tipo:
            Pedido.objects.create(
                nomepedido=nome,
                descpedido=desc,
                qtdpedido=qtd,
                statuspedido=status,
                datainicio=datainicio,
                datafim=datafim if datafim else None,
                produto_id=produto_id,
                tipopedido=tipo
            )
            return redirect('pedido')

    pedidos = Pedido.objects.select_related('produto')

    # Filtros aplicados
    if query:
        pedidos = pedidos.filter(nomepedido__icontains=query)
    if status_filter == 'finalizado':
        pedidos = pedidos.filter(statuspedido=2)
    elif status_filter == 'nao_finalizado':
        pedidos = pedidos.exclude(statuspedido=2)

    return render(request, 'estoque/pedido.html', {
        'produtos': produtos,
        'pedidos': pedidos,
        'query': query,
        'status_filter': status_filter,
    })

def editar_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, idpedido=pedido_id)
    produtos = Produto.objects.all()

    if request.method == 'POST':
        pedido.nomepedido = request.POST.get('nomepedido')
        pedido.descpedido = request.POST.get('descpedido')
        pedido.qtdpedido = request.POST.get('qtdpedido')
        pedido.statuspedido = request.POST.get('statuspedido')
        pedido.datainicio = request.POST.get('datainicio')
        pedido.datafim = request.POST.get('datafim')
        pedido.produto_id = request.POST.get('produto')
        pedido.tipopedido = request.POST.get('tipopedido')
        pedido.save()
        return redirect('pedido')

    return render(request, 'estoque/editar_pedido.html', {
        'pedido': pedido,
        'produtos': produtos,
        'produto': pedido.produto,  # ✅ Certifique-se da vírgula aqui
    })
