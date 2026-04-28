from django.shortcuts import render
from .models import Licenciatura, Docente, UnidadeCurricular, Tecnologia, Projeto, Competencia, Formacao, TFC, MakingOf, Projeto
from .forms import ProjetoForm

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

from django.shortcuts import render, redirect
from .forms import ProjetoForm, TecnologiaForm, CompetenciaForm, FormacaoForm

# ── PROJETO ──
def projeto_criar(request):
    form = ProjetoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Novo Projeto'})

def projeto_editar(request, pk):
    projeto = Projeto.objects.get(pk=pk)
    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Editar Projeto'})

def projeto_apagar(request, pk):
    projeto = Projeto.objects.get(pk=pk)
    if request.method == 'POST':
        projeto.delete()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/projeto_confirmar_apagar.html', {'objeto': projeto})

def tecnologia_criar(request):
    form = TecnologiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/form_generico.html', {'form': form, 'titulo': 'Nova Tecnologia'})

def tecnologia_editar(request, pk):
    tecnologia = Tecnologia.objects.get(pk=pk)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tecnologia)
    if form.is_valid():
        form.save()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/form_generico.html', {'form': form, 'titulo': 'Editar Tecnologia'})

def tecnologia_apagar(request, pk):
    tecnologia = Tecnologia.objects.get(pk=pk)
    if request.method == 'POST':
        tecnologia.delete()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/confirmar_apagar.html', {'objeto': tecnologia})


def competencia_criar(request):
    form = CompetenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:competencias')
    return render(request, 'portfolio/form_generico.html', {'form': form, 'titulo': 'Nova Competência'})

def competencia_editar(request, pk):
    competencia = Competencia.objects.get(pk=pk)
    form = CompetenciaForm(request.POST or None, instance=competencia)
    if form.is_valid():
        form.save()
        return redirect('portfolio:competencias')
    return render(request, 'portfolio/form_generico.html', {'form': form, 'titulo': 'Editar Competência'})

def competencia_apagar(request, pk):
    competencia = Competencia.objects.get(pk=pk)
    if request.method == 'POST':
        competencia.delete()
        return redirect('portfolio:competencias')
    return render(request, 'portfolio/confirmar_apagar.html', {'objeto': competencia})


def formacao_criar(request):
    form = FormacaoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:formacoes')
    return render(request, 'portfolio/form_generico.html', {'form': form, 'titulo': 'Nova Formação'})

def formacao_editar(request, pk):
    formacao = Formacao.objects.get(pk=pk)
    form = FormacaoForm(request.POST or None, request.FILES or None, instance=formacao)
    if form.is_valid():
        form.save()
        return redirect('portfolio:formacoes')
    return render(request, 'portfolio/form_generico.html', {'form': form, 'titulo': 'Editar Formação'})

def formacao_apagar(request, pk):
    formacao = Formacao.objects.get(pk=pk)
    if request.method == 'POST':
        formacao.delete()
        return redirect('portfolio:formacoes')
    return render(request, 'portfolio/confirmar_apagar.html', {'objeto': formacao})

def sobre_view(request):
    from .models import TipoTecnologia
    tipos = TipoTecnologia.objects.prefetch_related('tecnologias').all()
    makingofs = MakingOf.objects.all()
    return render(request, 'portfolio/sobre.html', {'tipos': tipos, 'makingofs': makingofs})