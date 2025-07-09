from django.db import models

class Produto(models.Model):
    idproduto = models.AutoField(primary_key=True)
    descproduto = models.CharField(max_length=255)
    estoqueproduto = models.IntegerField()
    unidadedemedida = models.CharField(max_length=50)

    class Meta:
        db_table = 'tabelaestoque'

class Pedido(models.Model):
    STATUS_CHOICES = [
        (1, 'Aberto'),
        (2, 'Finalizado'),
        (3, 'Cancelado'),
    ]
    TIPO_CHOICES = [
        (1, 'Compra de insumos'),
        (2, 'Produção de itens'),
    ]

    idpedido = models.AutoField(primary_key=True)
    nomepedido = models.CharField(max_length=20)
    descpedido = models.CharField(max_length=50, blank=True, null=True)
    qtdpedido = models.DecimalField(max_digits=10, decimal_places=2)
    statuspedido = models.IntegerField(choices=STATUS_CHOICES)
    datainicio = models.DateField()
    datafim = models.DateField(blank=True, null=True)
    produto = models.ForeignKey(Produto, db_column='tabelaestoqueidproduto', on_delete=models.CASCADE)
    tipopedido = models.IntegerField(choices=TIPO_CHOICES)

    class Meta:
        db_table = 'tabelapedido'

    def __str__(self):
        return self.nomepedido
