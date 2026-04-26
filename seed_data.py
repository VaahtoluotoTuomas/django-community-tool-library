import os
import django
from datetime import timedelta
import random
from django.utils import timezone

# Käynnistetään django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lainaamo_config.settings')
django.setup()

# Tuodaan mallit
from tyokalut.models import Manufacturer, Tag, Tool, Loan # noqa
from django.contrib.auth.models import User # noqa

def run_seed():
    print("Starting seeding...")

    # --- KÄYTTÄJÄT (TALOYHTIÖN VÄKI) ---
    users_data = ['seppo_talonmies', 'asunto_a1_olli', 'asunto_b14_marja', 'asunto_c22_tiina']
    users = []
    for username in users_data:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('testisalasana123')
            user.save()
        users.append(user)
    print("Users created.")

    # --- VALMISTAJAT ---
    manufacturers_data = [
        'Bosch', 'Makita', 'Kärcher', 'Fiskars', 'Ryobi', 
        'DeWalt', 'Knipex', 'Stihl', 'Black&Decker', 'Muu merkitön'
    ]
    manufacturers = {}
    for name in manufacturers_data:
        obj, _ = Manufacturer.objects.get_or_create(name=name)
        manufacturers[name] = obj
    print("Manufacturers created.")
    
    # --- TAGIT ---
    tags_data = [
        'Puutarha', 'Siivous', 'Sähkötyökalut', 'Remontointi', 
        'Käsityökalut', 'Maalaus', 'Autonlaitto', 'LVI', 'Pihatyöt'
    ]
    tags = {}
    for name in tags_data:
        obj, _ = Tag.objects.get_or_create(name=name)
        tags[name] = obj
    print("Tags created.")

    # --- TYÖKALUT (30 KPL TALOYHTIÖN LAINAAMOON) ---
    Tool.objects.all().delete()

    tools_info = [
        {"name": "Iskuporakone", "mfg": "Bosch", "year": 2020, "tags": ["Sähkötyökalut", "Remontointi"], "desc": "Seppon järeä porakone betonin poraamiseen. Terät löytyy salkusta, palauta puhtaana!"},
        {"name": "Tekstiilipesuri", "mfg": "Kärcher", "year": 2023, "tags": ["Siivous"], "desc": "B-portaan Marjan pesuri. Saa lainata, mutta osta omat pesuaineet. Ei eläintalouksiin, kiitos."},
        {"name": "Akkutrimmeri", "mfg": "Makita", "year": 2021, "tags": ["Puutarha", "Sähkötyökalut", "Pihatyöt"], "desc": "Taloyhtiön yhteinen trimmeri pihan siistimiseen. Akun laturi pyöräkellarissa."},
        {"name": "Halkaisukirves", "mfg": "Fiskars", "year": 2019, "tags": ["Puutarha", "Käsityökalut"], "desc": "Klassinen X21 kirves takkapuiden tekoon. Teroitettu viime syksynä. -Olli A1"},
        {"name": "Tasohiomakone", "mfg": "Ryobi", "year": 2024, "tags": ["Sähkötyökalut", "Remontointi", "Maalaus"], "desc": "Tiinan (C22) uusi hiomakone pintojen viimeistelyyn. Mukana muutama santapaperi."},
        {"name": "Oksasilppuri", "mfg": "Bosch", "year": 2018, "tags": ["Puutarha", "Pihatyöt"], "desc": "Kevät- ja syystalkoiden vakiovaruste. Pidä sormet kaukana teristä!"},
        {"name": "Painepesuri", "mfg": "Kärcher", "year": 2022, "tags": ["Siivous", "Autonlaitto"], "desc": "Taloyhtiön pesuri auton tai mattojen pesuun. Vesiletku löytyy roskakatoksen takaa."},
        {"name": "Akkuporakone", "mfg": "DeWalt", "year": 2023, "tags": ["Sähkötyökalut", "Remontointi"], "desc": "Ollin luottopeli. Sopii IKEAn huonekalujen kasaamiseen paremmin kuin hyvin."},
        {"name": "Moottorisaha", "mfg": "Stihl", "year": 2015, "tags": ["Puutarha", "Pihatyöt"], "desc": "Seppon vanha saha. Lainataan vain kokeneille käyttäjille! Tuo omat bensat."},
        {"name": "Tapetinirrotin", "mfg": "Bosch", "year": 2021, "tags": ["Remontointi"], "desc": "Pelasti mun olohuoneen remontin! Höyryttää tapetit irti seinästä hetkessä. -Marja B14"},
        {"name": "Höyrypesuri", "mfg": "Kärcher", "year": 2020, "tags": ["Siivous"], "desc": "Tiinan pesuri. Kylppärin kaakelit ja saumat saa tällä todella puhtaaksi ilman kemikaaleja."},
        {"name": "Kulmahiomakone", "mfg": "Makita", "year": 2017, "tags": ["Sähkötyökalut", "Remontointi"], "desc": "Taloyhtiön rälläkkä. Muista ehdottomasti käyttää suojalaseja! (Löytyy salkusta)."},
        {"name": "Jiirisaha", "mfg": "DeWalt", "year": 2022, "tags": ["Sähkötyökalut", "Remontointi"], "desc": "Ollin jiirisaha lattialistojen leikkaukseen. Todella painava, tarvitset kantoapua."},
        {"name": "Kelaruohonleikkuri", "mfg": "Fiskars", "year": 2020, "tags": ["Puutarha", "Pihatyöt"], "desc": "Äänetön käsikäyttöinen leikkuri takapihoille. Ei herätä naapureita sunnuntaiaamuna!"},
        {"name": "Lehtipuhallin", "mfg": "Ryobi", "year": 2023, "tags": ["Puutarha", "Pihatyöt"], "desc": "Akkukäyttöinen puhallin. Akku kestää noin 20 minuuttia teholla. -Tiina C22"},
        {"name": "Putkipihdit", "mfg": "Knipex", "year": 2010, "tags": ["Käsityökalut", "LVI"], "desc": "Seppon pakista. Hajulukkojen availuun ja muihin putkihommiin. Älä väännä liian lujaa."},
        {"name": "Momenttiavain", "mfg": "Black&Decker", "year": 2021, "tags": ["Käsityökalut", "Autonlaitto"], "desc": "Renkaanvaihtosesongin hitti! Palauta heti kun olet valmis, tälle on aina jonoa. -Olli"},
        {"name": "Pensasleikkuri", "mfg": "Makita", "year": 2019, "tags": ["Puutarha", "Pihatyöt"], "desc": "Taloyhtiön aitojen leikkaamiseen. Varo johtoa, se on jo kerran teipattu..."},
        {"name": "Kuumailmapuhallin", "mfg": "Bosch", "year": 2016, "tags": ["Sähkötyökalut", "Maalaus", "Remontointi"], "desc": "Maalin irrotukseen vanhoista ovista tai ikkunanpokista. Erittäin kuuma, varo palovaaraa."},
        {"name": "Ristilinjalaser", "mfg": "Bosch", "year": 2022, "tags": ["Remontointi", "Käsityökalut"], "desc": "Marjan laser. Helpottaa taulujen ja hyllyjen saamista suoraan linjaan. Toimii AA-paristoilla."},
        {"name": "Sorkkarauta", "mfg": "Fiskars", "year": 2012, "tags": ["Käsityökalut", "Remontointi"], "desc": "Iso rauta purkuhommiin. Löytyy Seppon varastosta kopin takaa."},
        {"name": "Oksasaha (varsisaha)", "mfg": "Fiskars", "year": 2021, "tags": ["Puutarha", "Pihatyöt"], "desc": "Teleskooppivarsi yltää pihan omenapuiden latvaan asti ilman tikkaita."},
        {"name": "A-Tikkaat", "mfg": "Muu merkitön", "year": 2015, "tags": ["Remontointi", "Siivous"], "desc": "Taloyhtiön yhteiset alumiinitikkaat. Säilytetään A-rapun pyöräkellarissa. Palauta aina paikalleen!"},
        {"name": "Kuusiokoloavainsarja", "mfg": "Knipex", "year": 2023, "tags": ["Käsityökalut", "Remontointi"], "desc": "Tiinan avaussarja. Kaikki koot tallella, huolehdi että pienin avain ei huku pimeisiin nurkkiin."},
        {"name": "Sähköhöylä", "mfg": "Makita", "year": 2018, "tags": ["Sähkötyökalut", "Remontointi"], "desc": "Turvonneiden ovien lyhentämiseen. Pitää kovaa meteliä, älä käytä hiljaisuuden aikaan. -Olli"},
        {"name": "Betonisekoitin", "mfg": "Muu merkitön", "year": 2005, "tags": ["Remontointi", "Pihatyöt"], "desc": "Taloyhtiön vanha mylly. Pihavarastossa, kysy Sepolta avain. Puhdista huolella heti käytön jälkeen!"},
        {"name": "Viemärinavausjousi", "mfg": "Muu merkitön", "year": 2018, "tags": ["Käsityökalut", "LVI"], "desc": "Inhottava homma, mutta tämä auttaa tukkoisiin lattiakaivoihin. PESE HYVIN käytön jälkeen!! -Seppo"},
        {"name": "Nokkakärryt", "mfg": "Muu merkitön", "year": 2019, "tags": ["Muut"], "desc": "Loistava apu muutoissa tai painavien laatikoiden siirrossa. Löytyy B-rapun portaiden alta."},
        {"name": "Ikkunapesuri", "mfg": "Kärcher", "year": 2022, "tags": ["Siivous"], "desc": "Tiinan akkukäyttöinen pesuri kevätpesuihin. Imee likaveden suoraan säiliöön, ei sotkua."},
        {"name": "Kottikärryt", "mfg": "Muu merkitön", "year": 2010, "tags": ["Puutarha", "Pihatyöt"], "desc": "Taloyhtiön yhteiset kärryt mullan ja haravointijätteen kuskaamiseen roskakatokselle."}
    ]

    tools = []
    for info in tools_info:
        tool = Tool.objects.create(
            name=info["name"],
            acquisition_year=info["year"],
            description=info["desc"]
        )
        tool.manufacturers.add(manufacturers[info["mfg"]])
        # Katsotaan ohitetaanko tuntemattomat tagit varmuuden vuoksi, jos niitä ei oltu luotu ylempänä
        for t in info.get("tags", []):
            if t in tags:
                tool.tags.add(tags[t])
        tools.append(tool)
    print(f"{len(tools)} Tools created.")

    # --- LAINAUKSET ---
    Loan.objects.all().delete()

    # Luodaan muutama historiallinen lainaus (esim. työkalut jo palautettu)
    hist_loan1 = Loan.objects.create(user=users[1], tool=tools[0]) # Olli lainasi Seppon porakonetta
    hist_loan1.borrowed_at = timezone.now() - timedelta(days=20)
    hist_loan1.returned_at = timezone.now() - timedelta(days=15)
    hist_loan1.save()

    hist_loan2 = Loan.objects.create(user=users[2], tool=tools[1]) # Marja testasi pesuriaan (itse)
    hist_loan2.borrowed_at = timezone.now() - timedelta(days=60)
    hist_loan2.returned_at = timezone.now() - timedelta(days=58)
    hist_loan2.save()

    # Luodaan muutama aktiivinen lainaus (työkalut tällä hetkellä jollain)
    Loan.objects.create(user=users[3], tool=tools[6]) # Tiinalla on taloyhtiön painepesuri
    Loan.objects.create(user=users[1], tool=tools[16]) # Ollilla on momenttiavain parhaillaan

    print("Loans created.")
    print("Data seeding successful! The database is now populated.")

if __name__ == '__main__':
    run_seed()