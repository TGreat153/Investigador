from django.db import models

# Create your models here.
class Contratos(models.Model):
    numero_contrato = models.CharField(max_length=100)
    nome_empresa = models.CharField(max_length=100)
    objeto = models.CharField(max_length=100)
    sei = models.CharField(max_length=100)
    gestor = models.CharField(max_length=100)
    fiscal = models.CharField(max_length=100)
    data_i = models.DateField()
    data_f = models.DateField()
    vigencia = models.IntegerField()
    valor = models.DecimalField(decimal_places=2,max_digits=100)
    fixo = models.BooleanField()
    ind = models.BooleanField()

    def __str__(self):
        return self.numero_contrato, self.nome_empresa, self.objeto, self.sei, self.gestor, self.fiscal

class Visualizar(models.Model):
    numero_contrato = models.CharField(max_length=100)
    mes = models.CharField(max_length=100)
    saldo = models.DecimalField(decimal_places=2, max_digits=10)
    acumulado = models.DecimalField(decimal_places=2, max_digits=10)
    restante = models.DecimalField(decimal_places=2,max_digits=10)
    porcem = models.FloatField()
    total = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return self.numero_contrato, self.mes