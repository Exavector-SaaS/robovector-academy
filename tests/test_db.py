import pytest
from django.db import connection


@pytest.mark.django_db
def test_db_connection():
    """Test to verify database connectivity."""
    cursor = connection.cursor()
    assert cursor is not None
