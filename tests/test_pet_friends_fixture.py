from api import PetFriends
from settings import valid_email, valid_password
import pytest

pf = PetFriends()


@pytest.fixture()
def get_key(self):
    self.pf = PetFriends()
    status, self.key = self.pf.get_api_key(email=valid_email, password=valid_password)
    assert status == 200
    assert 'key' in self.key
    return self.key


def test_get_all_pets_with_valid_key(self, get_key, filter=''):
    """Вводим валидные email и password и получаем список питомцев"""
    status, result = self.pf.get_list_of_pets(self.key, filter)

    # Проверяем соответствие ответа с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) > 0


