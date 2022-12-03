from django.shortcuts import render
from django.http import HttpResponse
from .models import Tecnologias, Empresa, Vagas
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants

def nova_empresa(request):
  if request.method == "GET":
    empresasCount = Empresa.objects.count()
    techs = Tecnologias.objects.all()
    return render(request, 'nova_empresa.html', {'techs':techs, 'empresaCount':empresasCount})
  elif request.method == "POST":
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    cidade = request.POST.get('cidade')
    endereco = request.POST.get('endereco')
    nicho = request.POST.get('nicho')
    caracteristicas = request.POST.get('caracteristicas')
    tecnologias = request.POST.getlist('tecnologias')
    logo = request.FILES.get('logo')
    
    if (len(nome.strip()) == 0 or len(email.strip()) == 0 or len(cidade.strip()) == 0 or len(endereco.strip()) == 0 or len(nicho.strip()) == 0 or len(caracteristicas.strip()) == 0 or (not logo)): 
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
      return redirect('/home/nova_empresa')

    if logo.size > 100_000_000:
      messages.add_message(request, constants.ERROR, 'A logo da empresa deve ter menos de 10MB')
      return redirect('/home/nova_empresa')

    if nicho not in [i[0] for i in Empresa.choices_nicho_mercado]:
      messages.add_message(request, constants.ERROR, 'Nicho de mercado inválido')
      return redirect('/home/nova_empresa')
    
    empresa = Empresa(logo=logo,
                        nome=nome,
                        email=email,
                        cidade=cidade,
                        endereco=endereco,
                        nicho_mercado=nicho,
                        caracteristica_empresa=caracteristicas)
    empresa.save()
    empresa.tecnologias.add(*tecnologias)
    empresa.save()
    
    messages.add_message(request, constants.SUCCESS, 'Empresa cadastrada com sucesso!')
    return redirect('/home/nova_empresa')
  
def empresas(request):
  tecnologias_filtro = request.GET.get('tecnologias')
  nome_filtro = request.GET.get('nome')
  empresas = Empresa.objects.all()
  
  if tecnologias_filtro:
    empresas = empresas.filter(tecnologias=tecnologias_filtro)
  
  if nome_filtro:
    empresas = empresas.filter(nome__icontains=nome_filtro)
  
  tecnologias = Tecnologias.objects.all()
  return render(request, 'empresas.html', {'empresas':empresas, 'tecnologias':tecnologias})

def empresa(request, id):
  empresa_unica = get_object_or_404(Empresa, id=id)
  empresas = Empresa.objects.all()
  tecnologias = Tecnologias.objects.all()
  vagas = Vagas.objects.filter(empresa_id=id)
  return render(request, 'empresa.html', {'empresa':empresa_unica,
                                          'tecnologias':tecnologias,
                                          'empresas':empresas,
                                          'vagas':vagas
                                          }
                )

def excluir_empresa(request, id):
  empresa = Empresa.objects.get(id=id)
  empresa.delete()
  messages.add_message(request, constants.SUCCESS, 'Empresa deletada com sucesso!')
  return redirect('/home/empresas')
