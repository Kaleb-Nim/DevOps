
"""
Test how app handles unexpected errors via the error handler
"""
from io import BytesIO

import pytest

@pytest.mark.parametrize(
    "endpoint",
    [
        ("forms", 200),
        ("history", 200),
        ("", 200),
        ("zzzzzzz", 404),
        ("home", 200),
    ],
)
def test_route_codes(client, endpoint, capsys):
    with capsys.disabled():
        endpoint, code = endpoint[0], endpoint[1]
        response = client.get(f"/{endpoint}")
        assert response.status_code == code