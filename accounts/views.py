from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistoForm, LoginForm, MagicLinkForm
from .models import MagicLinkToken


def login_view(request):
    form_login = LoginForm()
    form_magic = MagicLinkForm()

    if request.method == 'POST':
        if 'login_senha' in request.POST:
            form_login = LoginForm(request.POST)
            if form_login.is_valid():
                user = authenticate(
                    request,
                    username=form_login.cleaned_data['username'],
                    password=form_login.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    return redirect(request.GET.get('next', 'portfolio:projetos'))
                else:
                    messages.error(request, 'Utilizador ou password incorretos.')

        elif 'magic_link' in request.POST:
            form_magic = MagicLinkForm(request.POST)
            if form_magic.is_valid():
                try:
                    user = User.objects.get(email=form_magic.cleaned_data['email'])
                    token_obj = MagicLinkToken.create_for_user(user)
                    link = request.build_absolute_uri(f'/accounts/magic/{token_obj.token}/')
                    # Em produção enviaria email; aqui mostramos o link para testar
                    messages.success(request, f'Link mágico gerado! Para testar acede a: {link}')
                except User.DoesNotExist:
                    messages.success(request, 'Se o email estiver registado, receberás um link.')

    return render(request, 'accounts/login.html', {
        'form_login': form_login,
        'form_magic': form_magic,
    })


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def registo_view(request):
    form = RegistoForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        grupo_autores, _ = Group.objects.get_or_create(name='autores')
        user.groups.add(grupo_autores)
        login(request, user)
        messages.success(request, f'Bem-vindo, {user.username}!')
        return redirect('portfolio:projetos')
    return render(request, 'accounts/registo.html', {'form': form})


def magic_link_verify(request, token):
    try:
        token_obj = MagicLinkToken.objects.select_related('user').get(token=token)
        if token_obj.is_valid():
            token_obj.used = True
            token_obj.save()
            login(request, token_obj.user,
                  backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Bem-vindo, {token_obj.user.username}!')
            return redirect('portfolio:projetos')
        else:
            messages.error(request, 'Este link já foi usado ou expirou.')
    except MagicLinkToken.DoesNotExist:
        messages.error(request, 'Link inválido.')
    return redirect('accounts:login')


@login_required
def perfil_view(request):
    return render(request, 'accounts/perfil.html')