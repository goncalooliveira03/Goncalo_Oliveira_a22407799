def user_groups(request):
    is_gestor = False
    is_autor = False
    if request.user.is_authenticated:
        grupos = request.user.groups.values_list('name', flat=True)
        is_gestor = 'gestor-portfolio' in grupos
        is_autor = 'autores' in grupos
    return {
        'is_gestor_portfolio': is_gestor,
        'is_autor': is_autor,
    }