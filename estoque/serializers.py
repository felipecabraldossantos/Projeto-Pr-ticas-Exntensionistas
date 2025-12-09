from rest_framework import serializers
from .models import Produto, Pedido

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['idproduto', 'descproduto', 'estoqueproduto', 'unidadedemedida']
