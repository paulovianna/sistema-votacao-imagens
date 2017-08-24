from models import *
from django.contrib import admin


class FotoAdmin(admin.ModelAdmin):
    list_display = ('autor', 'total_votos')


admin.site.register(Voto)
admin.site.register(Categoria)
admin.site.register(Foto, FotoAdmin)
admin.site.register(VotoCPF)
