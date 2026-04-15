from django.shortcuts import render
from .models import Licenciatura, Docente, UnidadeCurricular, Tecnologia, Projeto, Competencia, Formacao, TFC, MakingOf

def index(request):
    return render(request, 'portfolio/index.html')

def licenciaturas_view(request):
    licenciaturas = Licenciatura.objects.prefetch_related('ucs').all()
    return render(request, 'portfolio/licenciaturas.html', {'licenciaturas': licenciaturas})

def docentes_view(request):
    docentes = Docente.objects.prefetch_related('ucs', 'tfcs').all()
    return render(request, 'portfolio/docentes.html', {'docentes': docentes})

def ucs_view(request):
    ucs = UnidadeCurricular.objects.select_related('licenciatura').prefetch_related('docentes', 'projetos').all()
    return render(request, 'portfolio/ucs.html', {'ucs': ucs})

def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})

def projetos_view(request):
    projetos = Projeto.objects.select_related('unidade_curricular').prefetch_related('tecnologias').all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})

def competencias_view(request):
    competencias = Competencia.objects.prefetch_related('tecnologias', 'projetos').all()
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})

def formacoes_view(request):
    formacoes = Formacao.objects.prefetch_related('competencias').all()
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})

def tfcs_view(request):
    tfcs = TFC.objects.select_related('orientador').all()
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})

def makingof_view(request):
    makingofs = MakingOf.objects.all()
    return render(request, 'portfolio/makingof.html', {'makingofs': makingofs})