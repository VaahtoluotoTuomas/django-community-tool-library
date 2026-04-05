import os
import django
from datetime import timedelta
from django.utils import timezone

# käynnistetään django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lainaamo_config.settings')
django.setup()

# tuodaan mallit
from tyokalut.models import Manufacturer, Tag, Tool, Loan # noqa
from django.contrib.auth.models import User # noqa

def run_seed():
    print("Starting seeding...")

    # --- KÄYTTÄJÄT ---
    users_data = ['matti_meikalainen', 'maija_naapuri', 'pekka_puutarhuri']
    users = []
    for username in users_data:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('testisalasana123')
            user.save()
        users.append(user)
    print("Users created.")

    # --- VALMISTAJAT ---
    manufacturers_data = ['Bosch', 'Makita', 'Kärcher', 'Fiskars', 'Ryobi']
    manufacturers = {}
    for name in manufacturers_data:
        obj, _ = Manufacturer.objects.get_or_create(name=name)
        manufacturers[name] = obj
    print("Manufacturers created.")
    
    # --- TAGIT ---
    tags_data = ['Puutarha', 'Siivous', 'Sähkötyökalut', 'Remontointi', 'Käsityökalut']
    tags = {}
    for name in tags_data:
        obj, _ = Tag.objects.get_or_create(name=name)
        tags[name] = obj
    print("Tags created.")

    # --- TOOLS ---
    Tool.objects.all().delete()

    tools_info = [
        {"name": "Iskuporakone", "mfg": "Bosch", "year": 2022, "tags": ["Sähkötyökalut", "Remontointi"], "desc": "Tehokas porakone betonin poraamiseen."},
        {"name": "Tekstiilipesuri", "mfg": "Kärcher", "year": 2023, "tags": ["Siivous"], "desc": "Tällä lähtee sohvista ja matoista sitkeimmätkin tahrat."},
        {"name": "Akkutrimmeri", "mfg": "Makita", "year": 2021, "tags": ["Puutarha", "Sähkötyökalut"], "desc": "Kevyt trimmeri pihan siistimiseen."},
        {"name": "Halkaisukirves", "mfg": "Fiskars", "year": 2019, "tags": ["Puutarha", "Käsityökalut"], "desc": "Klassinen X21 kirves polttopuiden tekoon."},
        {"name": "Tasohiomakone", "mfg": "Ryobi", "year": 2024, "tags": ["Sähkötyökalut", "Remontointi"], "desc": "Akkukäyttöinen hiomakone pintojen viimeistelyyn."}
    ]

    tools = []
    for info in tools_info:
        tool = Tool.objects.create(
            name=info["name"],
            acquisition_year=info["year"],
            description=info["desc"]
        )
        tool.manufacturers.add(manufacturers[info["mfg"]])
        for t in info["tags"]:
            tool.tags.add(tags[t])
        tools.append(tool)
    print("Tools created.")

    # --- LOANS ---
    Loan.objects.all().delete()

    hist_loan = Loan.objects.create(
        user=users[0],
        tool=tools[1]
    )
    hist_loan.borrowed_at = timezone.now() - timedelta(days=20)
    hist_loan.returned_at = timezone.now() - timedelta(days=15)
    hist_loan.save()

    Loan.objects.create(user=users[1], tool=tools[0])
    Loan.objects.create(user=users[2], tool=tools[3])

    print("Loan created.")
    print("Data seeding succesful! The database is now populated.")

if __name__ == '__main__':
    run_seed()