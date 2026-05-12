import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.files import File
from django.conf import settings
from portfolio.models import Licenciatura, Docente, UnidadeCurricular, Tecnologia, Projeto, Formacao, MakingOf
from artigos.models import Artigo
from curso.models import Curso

def migrar(queryset, campo):
    for obj in queryset:
        field = getattr(obj, campo)
        if field and field.name:
            try:
                local_path = os.path.join(settings.MEDIA_ROOT, field.name)
                if os.path.exists(local_path):
                    with open(local_path, 'rb') as f:
                        field.save(os.path.basename(local_path), File(f), save=True)
                    print(f"✅ Migrado: {obj} ({campo})")
                else:
                    print(f"⚠️  Ficheiro não encontrado: {local_path}")
            except Exception as e:
                print(f"❌ Erro em {obj}: {e}")

migrar(Licenciatura.objects.all(), 'logo')
migrar(Docente.objects.all(), 'fotografia')
migrar(UnidadeCurricular.objects.all(), 'imagem')
migrar(Tecnologia.objects.all(), 'logo')
migrar(Projeto.objects.all(), 'imagem')
migrar(Formacao.objects.all(), 'certificado')
migrar(MakingOf.objects.all(), 'fotografia')
migrar(Artigo.objects.all(), 'fotografia')
migrar(Curso.objects.all(), 'imagem')

print("\nMigração concluída!")