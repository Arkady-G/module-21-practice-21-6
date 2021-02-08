from api import PetFriends
from settings import valid_email, valid_password
import pytest
import os

pf = PetFriends()


class TestPetFriends:

    @pytest.fixture(autouse=True)
    def get_key(self):
        self.pf = PetFriends()
        status, self.key = pf.get_api_key(email=valid_email, password=valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

        assert self.status == 200

    def test_get_all_pets_with_valid_key(self, get_key, filter=''):
        """Вводим валидные email и password и получаем список питомцев"""
        self.status, result = self.pf.get_list_of_pets(self.key, filter)

        # Проверяем соответствие ответа с ожидаемым результатом
        assert len(result['pets']) > 0

    def test_add_new_pet_with_valid_data(self, get_key, name='Барон', animal_type='кот', age='1',
                                         pet_photo='images/Maine_Coon_001.jpg'):
        """Проверяем добавление питомца"""
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Добавляем питомца
        self.status, result = self.pf.add_new_pet(self.key, name, animal_type, age, pet_photo)

        # Проверяем соответствие ответа с ожидаемым результатом

        assert result['name']

    def test_successfull_delete_self_pet(self, get_key):
        """Проверяем удаление пиомца по ID"""
        # Запрашиваем ключ auth_key и запрашиваем список моих питомцев
        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')

        # Проверяем список моих питомцев. Если список пустой - добавляем питомца и снова проверяем список моих питомцев
        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet(self.key, 'Барон', 'кот', '1', 'images/Maine_Coon_001.jpg')
            _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')

        pet_id = my_pets['pets'][0]['id']
        self.status, _ = self.pf.delete_pet(self.key, pet_id)

        # Еще раз запрашиваем список своих питомцев
        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')

        # Проверяем статус ответа и отсутствие в списке id удаленного питомца

        assert pet_id not in my_pets.values()
