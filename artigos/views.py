from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artigo, Comentario
from .forms import ArtigoForm, ComentarioForm


def lista_artigos(request):
    artigos = Artigo.objects.select_related('autor').all()
    return render(request, 'artigos/lista.html', {'artigos': artigos})


def detalhe_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    form_comentario = ComentarioForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            comentario = form_comentario.save(commit=False)
            comentario.artigo = artigo
            comentario.autor = request.user
            comentario.save()
            return redirect('artigos:detalhe', pk=pk)

    ja_gostou = request.user.is_authenticated and artigo.likes.filter(pk=request.user.pk).exists()
    return render(request, 'artigos/detalhe.html', {
        'artigo': artigo,
        'form_comentario': form_comentario,
        'ja_gostou': ja_gostou,
    })


@login_required
def criar_artigo(request):
    if not request.user.groups.filter(name='autores').exists():
        messages.error(request, 'Apenas autores podem publicar artigos.')
        return redirect('artigos:lista')
    form = ArtigoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        return redirect('artigos:detalhe', pk=artigo.pk)
    return render(request, 'artigos/form.html', {'form': form, 'titulo': 'Novo Artigo'})


@login_required
def editar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if artigo.autor != request.user:
        messages.error(request, 'Só podes editar os teus próprios artigos.')
        return redirect('artigos:detalhe', pk=pk)
    form = ArtigoForm(request.POST or None, request.FILES or None, instance=artigo)
    if form.is_valid():
        form.save()
        return redirect('artigos:detalhe', pk=pk)
    return render(request, 'artigos/form.html', {'form': form, 'titulo': 'Editar Artigo'})


@login_required
def apagar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if artigo.autor != request.user:
        messages.error(request, 'Só podes apagar os teus próprios artigos.')
        return redirect('artigos:detalhe', pk=pk)
    if request.method == 'POST':
        artigo.delete()
        return redirect('artigos:lista')
    return render(request, 'artigos/confirmar_apagar.html', {'artigo': artigo})


def like_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.user.is_authenticated:
        if artigo.likes.filter(pk=request.user.pk).exists():
            artigo.likes.remove(request.user)
        else:
            artigo.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER', 'artigos:lista'))
    else:
        messages.info(request, 'Faz login para dar like.')
        return redirect('accounts:login')