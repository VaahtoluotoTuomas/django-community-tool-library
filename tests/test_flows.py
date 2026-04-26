import pytest
from django.urls import reverse
from tyokalut.models import Loan, Tool

@pytest.mark.django_db
class TestUserFlows:

    def test_full_borrow_and_return_flow(self, client, test_user, tool_item):
        """
        Kattava integraatiotesti, joka simuloi koko työkalun lainaus- ja palautuskaaren
        loppukäyttäjän näkökulmasta Djangon testclientillä.
        """
        
        # Vaihe 1: Käyttäjä kirjautuu sisään
        # Käytämme Djangon client.force_login -metodia lomakkeen täytön sijaan
        # pitääksemme testin puhtaana ja keskittyneenä nimenomaan työkalu-logiikkaan.
        client.force_login(test_user)
        
        # Vaihe 2: Käyttäjä etsii 'Akkuporakoneen'
        search_url = reverse('tyokalu_lista')
        search_response = client.get(search_url, {'q': tool_item.name})
        assert search_response.status_code == 200
        # Varmistetaan, että hakutuloksista (DOM:ista) löytyy etsitty työkalu
        assert tool_item.name in search_response.content.decode('utf-8')
        
        # Vaihe 3: Käyttäjä avaa työkalun tiedot ja klikkaa lainausnappia (POST-pyyntö)
        details_url = reverse('tyokalu_tiedot', args=[tool_item.id])
        details_response = client.get(details_url)
        assert details_response.status_code == 200
        
        # Simuloidaan "Lainaa" -napin painallus (HTMX / lomake POST)
        borrow_url = reverse('lainaa_tyokalu', args=[tool_item.id])
        client.post(borrow_url)
        
        # Varmistetaan kantaan muodostunut uusi avoin laina-tietue
        assert Loan.objects.filter(user=test_user, tool=tool_item, returned_at__isnull=True).exists()
        
        # Varmistetaan, että työkalu on nyt poistunut vapaiden listalta
        tool_item.refresh_from_db()
        assert tool_item.is_available is False
        
        # Vaihe 4: Varmistetaan, että työkalu näkyy käyttäjän 'Omat lainat' -sivulla
        my_loans_url = reverse('omat_lainat')
        my_loans_response = client.get(my_loans_url)
        assert my_loans_response.status_code == 200
        assert tool_item.name in my_loans_response.content.decode('utf-8')
        
        # Haetaan luotu aktiivinen laina tietokannasta, jotta saamme sen ID:n palautusta varten
        active_loan = Loan.objects.get(user=test_user, tool=tool_item, returned_at__isnull=True)
        
        # Vaihe 5: Käyttäjä palauttaa työkalun (POST-pyyntö palautusnäkymään)
        return_url = reverse('palauta_tyokalu', args=[active_loan.id])
        client.post(return_url)
        
        # Varmistetaan tietokannasta, että lainan 'returned_at' -aika on leimattu 
        # ja työkalu on palautunut tilaltaan jälleen vapaaksi
        active_loan.refresh_from_db()
        assert active_loan.returned_at is not None
        
        tool_item.refresh_from_db()
        assert tool_item.is_available is True
