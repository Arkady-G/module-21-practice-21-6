from api import PetFriends
from settings import valid_email, valid_password
import pytest

pf = PetFriends()


@pytest.fixture(autouse=True)
def get_key(self):
    self.pf = PetFriends()
    status, self.key = pf.get_api_key(email=valid_email, password=valid_password)
    assert status == 200
    assert 'key' in self.key

    yield

    assert self.status == 200
