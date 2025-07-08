from django.db import models

class Produto(models.Model):
    idproduto = models.AutoField(primary_key=True)
    descproduto = models.CharField(max_length=255)
    estoqueproduto = models.IntegerField()
    unidadedemedida = models.CharField(max_length=50)

    class Meta:
        db_table = 'tabelaestoque'
