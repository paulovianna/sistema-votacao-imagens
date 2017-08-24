from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
from cpf import CPFField

saved_file.connect(generate_aliases_global)


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome
    
class Foto(models.Model):
    autor = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria)
    foto = models.ImageField(upload_to='images')

    def total_votos(self):
        return  VotoCPF.objects.filter(voto = self).count()

	
    def __unicode__(self):
        return u"%s - %s" % (self.categoria, self.autor)

    class Meta:
        ordering = ['categoria', 'id']
	

class Voto(models.Model):
    usuario = models.ForeignKey(User)
    categoria = models.ForeignKey(Categoria)
    voto = models.ForeignKey(Foto)

    def __unicode__(self):
        return self.voto


class VotoCPF(models.Model):
    usuario = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria)
    voto = models.ForeignKey(Foto)

    def __unicode__(self):
        return u"%s - %s" % (self.usuario, self.voto.autor)
