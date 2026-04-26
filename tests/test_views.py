import pytest
from django.urls import reverse
from tyokalut.models import Loan

@pytest.mark.django_db
class TestViews:

    # --- Sivujen lataus (Happy Path) ---

    def test_front_page_loads(self, client):
        """Testaa, että laitteiden listaus (etusivu) avautuu onnistuneesti."""
        # Arrange
        url = reverse('tyokalu_lista')
        
        # Act
        response = client.get(url)
        
        # Assert
        assert response.status_code == 200

    def test_tool_details_loads(self, client, tool_item):
        """Testaa, että yksittäisen työkalun tietosivu aukeaa oikein."""
        # Arrange
        url = reverse('tyokalu_tiedot', args=[tool_item.id])
        
        # Act
        response = client.get(url)
        
        # Assert
        assert response.status_code == 200


    # --- Pääsyhallinta (Critical Fail) ---

    def test_my_loans_requires_login(self, client):
        """Testaa, että Omat lainat -sivu ohjaa kirjautumattoman käyttäjän pois."""
        # Arrange
        url = reverse('omat_lainat')
        
        # Act
        response = client.get(url)
        
        # Assert (Status 302 ja ohjaus joko /login/ tai kirjaudu-sivulle)
        assert response.status_code == 302
        assert reverse('kirjaudu') in response.url or '/login' in response.url

    def test_borrow_tool_requires_login(self, client, tool_item):
        """Testaa, että kirjautumaton ei voi kutsua lainausrajapintaa lainatakseen työkalun."""
        # Arrange
        url = reverse('lainaa_tyokalu', args=[tool_item.id])
        
        # Act
        response = client.post(url)
        
        # Assert
        assert response.status_code == 302
        assert reverse('kirjaudu') in response.url or '/login' in response.url
        assert Loan.objects.count() == 0


    # --- Lainausprosessi (Integration) ---

    def test_logged_in_user_can_borrow_tool(self, client, test_user, tool_item):
        """Testaa onnistunut työkalun lainaus tunnistautuneena."""
        # Arrange
        client.force_login(test_user)
        url = reverse('lainaa_tyokalu', args=[tool_item.id])
        assert Loan.objects.count() == 0
        
        # Act
        response = client.post(url)
        
        # Assert
        # Usein HTMX-kutsut voivat palauttaa joko 200 (HTML-fragmentti) tai ohjauksen. 
        # Tärkein tae reitin onnistumisesta on tietokannan päivittyminen.
        assert Loan.objects.count() == 1
        loan = Loan.objects.first()
        assert loan.user == test_user
        assert loan.tool == tool_item


    # --- Haku ---

    def test_search_returns_correct_tool(self, client, tool_item):
        """Testaa, että hakukentän käyttö ('q'-parametri) palauttaa olemassa olevan työkalun nimen domiin."""
        # Arrange
        url = reverse('tyokalu_lista')
        
        # Act
        response = client.get(url, {'q': tool_item.name})
        
        # Assert
        assert response.status_code == 200
        # Tarkistetaan että haetun fixture-työkalun nimi (esim. Akkuporakone) esiintyy saadussa sivussa
        assert tool_item.name in response.content.decode('utf-8')
