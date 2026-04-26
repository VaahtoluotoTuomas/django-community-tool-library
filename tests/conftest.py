import pytest
from django.contrib.auth.models import User
from tyokalut.models import Tool

@pytest.fixture
def test_user(db):
    """Luo tavallinen testikäyttäjä."""
    return User.objects.create_user(username='test_user', password='password123')

@pytest.fixture
def tool_item(db):
    """Luo vapaana oleva työkalu."""
    return Tool.objects.create(
        name='Akkuporakone',
        acquisition_year=2020,
        description='Toimiva Makita 18V akkuporakone kahdella akulla.'
    )
