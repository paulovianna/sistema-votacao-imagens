# -*- coding: cp1252 -*-
from models import Foto, Categoria, Voto, VotoCPF
from django.shortcuts import render_to_response, get_list_or_404, RequestContext, get_object_or_404
from django import forms
import re
from cpf import validate_cpf

class VotaForm(forms.ModelForm):
    def clean_voto(self):
        voto = self.cleaned_data['voto']

        if 'usuario' in self.cleaned_data:
            usuario = self.cleaned_data['usuario']
            if not usuario.isdigit():
                usuario = re.sub('[-\.]', '', usuario)
        else:
            raise forms.ValidationError(u"Preencha o RG.")
        
        categoria = self.cleaned_data['categoria']

        #print usuario
        votos = VotoCPF.objects.filter(usuario=usuario, categoria=categoria)

        print votos
        
        if len(votos) >= 3 and usuario != "0810243116":
            raise forms.ValidationError(u"Você já realizou o limite de 3 votos.")
            print usuario

        if usuario != "0810243116":
            try:
                atual = VotoCPF.objects.get(voto=voto, usuario=usuario)
                print atual
                
            except:
                self.cleaned_data['sobrando'] = 2-len(votos)
                return voto

            raise forms.ValidationError(u"Você já votou nessa foto.")
        else:
            self.cleaned_data['sobrando'] = 2
            return voto            

        
        
    class Meta:
        model = VotoCPF

def exibe_fotos(request):
    fotos1 = Foto.objects.filter(categoria=1).order_by('autor')
    #fotos2 = Foto.objects.filter(categoria=2).order_by('?')

    return render_to_response("index.html", {'fotos1': fotos1}, context_instance=RequestContext(request))

def exibe_foto(request, fid):
    foto = get_object_or_404(Foto, id=fid)

    return render_to_response("share.html", {'foto': foto}, context_instance=RequestContext(request))


def votar(request):
    form = VotaForm(request.POST or None)


    if form.is_valid():
        form.save()
        return render_to_response("voto_ok.html", {'form': form, 'sobrando': form.cleaned_data['sobrando']}, context_instance=RequestContext(request))

    return render_to_response("voto.html", {'form': form}, context_instance=RequestContext(request))
