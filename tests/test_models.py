import pytest
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from tyokalut.models import Loan

@pytest.mark.django_db
class TestToolModel:

    def test_tool_creation_happy_path(self, tool_item):
        """Happy Path: Testataan, että työkalun luonti onnistuu ja se on oletuksena vapaana."""
        # Assert
        assert tool_item.id is not None
        assert tool_item.name == 'Akkuporakone'
        assert tool_item.is_available is True

    def test_tool_checkout_status_change(self, test_user, tool_item):
        """Happy Path: Testataan, että työkalun tila päivittyy automaattisesti lainatuksi."""
        # Arrange
        assert tool_item.is_available is True

        # Act
        Loan.objects.create(
            user=test_user,
            tool=tool_item,
            due_date=timezone.now() + timedelta(days=7)
        )

        # Assert
        assert tool_item.is_available is False

    def test_cannot_borrow_already_borrowed_tool(self, test_user, tool_item):
        """Critical Fail: Testataan, ettei jo lainassa olevaa työkalua voi lainata uudelleen."""
        # Arrange - Lainataan työkalu ensin testikäyttäjälle
        Loan.objects.create(
            user=test_user,
            tool=tool_item,
            due_date=timezone.now() + timedelta(days=7)
        )
        
        # TÄMÄ ON RATKAISU: Päivitä työkalun tila tietokannasta muistiin
        tool_item.refresh_from_db() 
        
        assert tool_item.is_available is False

        # Act & Assert
        with pytest.raises(ValidationError) as excinfo:
            Loan.objects.create(
                user=test_user,
                tool=tool_item,
                due_date=timezone.now() + timedelta(days=7)
            )
        
        assert "Tämä työkalu on jo lainassa." in str(excinfo.value)
