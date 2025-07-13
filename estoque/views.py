from django.shortcuts import render, redirect
from .models import Produto, Pedido, ContatoForm
from django.shortcuts import get_object_or_404,render, redirect
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/home.html', {'produtos': produtos})

@login_required
def estoque_view(request):
    query = request.GET.get('q')
    if query:
        produtos = Produto.objects.filter(descproduto__icontains=query)
    else:
        produtos = Produto.objects.all()
    return render(request, 'estoque/estoque.html', {'produtos': produtos})

@login_required
def produto_view(request):

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

@login_required
def editar_produto_view(request, produto_id):
    produto = produto = get_object_or_404(Produto, idproduto=produto_id)
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

@login_required
def editar_produto_redirect_view(request):
    produto_id = request.GET.get("produto_id")
    if produto_id:
        return redirect('editar_produto', produto_id=produto_id)
    return redirect('produto')

@login_required
def pedido_view(request):
    produtos = Produto.objects.all()
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    
    if request.method == 'POST' and 'selecionar_pedido' in request.POST:
        pedido_id = request.POST.get('pedido_selecionado')
        if pedido_id:
            return redirect('editar_pedido', pedido_id=pedido_id)

    
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

@login_required
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
        'produto': pedido.produto,
    })

@login_required
def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            mensagem = form.cleaned_data['mensagem']
            
            assunto = f'Contato de {nome}'
            corpo = f'Email: {email}\n\nMensagem:\n{mensagem}'

            send_mail(
                assunto,
                corpo,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER, settings.EMAIL_SUPORTE],
                fail_silently=False,
            )
            return redirect('contato_enviado')  # criar outra tela
    else:
        form = ContatoForm()
    
    return render(request, 'estoque/contato.html', {'form': form})

@login_required
def contato_enviado(request):
    return render(request, 'estoque/contato_enviado.html')
