import os
import sys
import django
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import Licenciatura, UnidadeCurricular

# Criar ou obter a Licenciatura LEI
licenciatura, created = Licenciatura.objects.get_or_create(
    sigla='LEI',
    defaults={
        'nome': 'Licenciatura em Engenharia Informática',
        'instituicao': 'Universidade Lusófona',
        'ano_inicio': 2022,
        'descricao': 'Licenciatura em Engenharia Informática na Universidade Lusófona de Lisboa.',
        'link': 'https://informatica.ulusofona.pt/ensino/licenciaturas/engenharia-informatica/',
    }
)
if created:
    print("✓ Licenciatura LEI criada")
else:
    print("✓ Licenciatura LEI já existia")

# Caminho para o JSON do curso em PT
json_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'data', 'files', 'ULHT260-PT.json'
)

with open(json_path, 'r', encoding='utf-8') as f:
    curso_data = json.load(f)

# Limpar UCs existentes para evitar duplicados
UnidadeCurricular.objects.filter(licenciatura=licenciatura).delete()

ucs_carregadas = 0

for uc in curso_data.get('courseFlatPlan', []):
    code = uc.get('curricularIUnitReadableCode', '')

    # Tentar ler o JSON de detalhe da UC
    uc_json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data', 'files', f"{code}-PT.json"
    )

    descricao = ''
    docente = ''

    if os.path.exists(uc_json_path):
        with open(uc_json_path, 'r', encoding='utf-8') as f:
            uc_detail = json.load(f)

        # Extrair descrição se existir
        if uc_detail.get('objectives'):
            descricao = uc_detail['objectives'][:500]

        # Extrair docente principal se existir
        docentes = uc_detail.get('responsibleTeacher', [])
        if docentes:
            docente = docentes[0].get('name', '') if isinstance(docentes, list) else str(docentes)

    UnidadeCurricular.objects.create(
        nome=uc.get('curricularUnitName', code),
        sigla=code,
        ano=uc.get('studyYear', 1),
        semestre=uc.get('semester', 1),
        ects=uc.get('ects', 6),
        descricao=descricao,
        docente=docente,
        licenciatura=licenciatura,
    )
    ucs_carregadas += 1
    print(f"  ✓ UC carregada: {uc.get('curricularUnitName', code)}")

print(f"\nTotal de UCs carregadas: {ucs_carregadas}")