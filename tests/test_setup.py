import pytest
import os
from django.conf import settings

def test_pytest_setup():
    """Tarkistaa että pytest toimii"""
    assert True

def test_django_connection():
    """Tarkistaa että pytest on ladannut Djangon asetukset oikein"""
    # Tarkistetaan ympäristömuuttuja
    assert os.environ.get('DJANGO_SETTINGS_MODULE') == "lainaamo_config.settings"
    # Tarkistetaan joku oikea asetus, esim. BASE_DIR tai DEBUG
    assert settings.SECRET_KEY is not None