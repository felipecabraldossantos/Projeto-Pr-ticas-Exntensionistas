from rest_framework import serializers
from .models import Produto, Pedido

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['idproduto', 'descproduto', 'estoqueproduto', 'unidadedemedida']


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'idpedido',
            'nomepedido',
            'descpedido',
            'qtdpedido',
            'statuspedido',
            'datainicio',
            'datafim',
            'produto',
            'tipopedido'
        ]
