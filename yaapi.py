import requests
import settings
from datetime import datetime


class YaApi:
    """
    Класс для работы с api яндекс диска
    """
    photos = []  # список фотографий для json дампа
    settings = settings.Settings()
    token_ya = settings.get_token_ya()

    def get_headers_ya(self):
        """
        Получение заголовка Яндекс Диск
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_ya}'
        }

    def make_dir_ya(self, dir_name):
        """
        Создание каталога на Яндекс Диске
        :param dir_name: название папки
        """
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers_ya()
        params = {
            'path': f'/{dir_name}'
        }
        requests.put(URL, headers=headers, params=params).json()

    def get_upload_link_ya(self, likes, size, directory='backup', exist=False):
        """
        Получаем ссылку на путь в Яндекс диск.
        Получаем имя файла.
        :param exist: True - файл с именем лайков существует
        :param likes: лайки
        :param size: размер фото
        :param directory: имя папки для создания и помещения в нее фото, по умолчанию backup
        :return: ссылка на путь Яндекс Диска
        """

        if exist:  # если файл существует
            date = datetime.now()
            date = f'{date.day}-{date.month}-{date.year}_{date.hour}-{date.minute}-{date.second}'
            name_of_file = f'{directory}/{likes}_{date}.jpg'
            for i in self.photos:
                if i['file_name'] == f'{directory}/{likes}.jpg':
                    self.photos.remove(i)
        else:  # если файл не существует
            name_of_file = f'{directory}/{likes}.jpg'

        # создаем каталог для копий фотографий в Яндекс Диске
        self.make_dir_ya(directory)

        URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers_ya()
        params = {
            'path': f'{name_of_file}',
            'overwrite': 'false'
        }
        req = requests.get(URL, headers=headers, params=params).json()

        self.photos.append({'file_name': name_of_file, 'size': size})

        return req['href']

    def upload_ya(self, photos_vk):
        """
        Загружаем фото на Яндекс Диск
        :param photos_vk: список get_photos(), [0] - лайки, [1] - линк на фото
        """
        url = photos_vk[1]
        data = requests.get(url)
        try:  # если файл не существует
            requests.put(url=self.get_upload_link_ya(likes=photos_vk[0], size=photos_vk[2]), data=data)
        except KeyError:  # если файл существует (добавляется параметр exist=True)
            requests.put(url=self.get_upload_link_ya(likes=photos_vk[0], size=photos_vk[2], exist=True), data=data)
