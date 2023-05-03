import requests
import settings
import sys


class VkApi:
    """
    Класс для работы с api вконтакте
    """
    settings = settings.Settings()
    token_vk = settings.get_token_vk()

    def __init__(self, count_for_download, owner_id="", screen_name=""):
        """
        :param owner_id: ID пользователя
        :param count_for_download: Количество фото для загрузки
        :param screen_name: Screen name пользователя
        """
        # Если не ввели ни owner_id, ни screen_name
        if owner_id == "" and screen_name == "":
            print('Ошибка! Необходимо ввести либо owner_id, либо screen_name.')
            sys.exit()

        self.count_for_download = count_for_download
        self.screen_name = screen_name
        # Если ввели screen_name, то id получаем через screen_name, а значение owner_id игнорируем
        if self.screen_name != "":
            self.owner_id = self.get_id_screen_name()
        else:
            self.owner_id = owner_id

    def get_id_screen_name(self):
        """
        Получение id пользователя вк по screen_name
        :return: id пользователя
        """
        URL = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
            'screen_name': self.screen_name,
            'access_token': self.token_vk,
            'v': '5.331'
        }

        req = requests.get(URL, params).json()
        return req['response']['object_id']

    def get_photos(self):
        """
        Получение списка фотографий вк
        :return: список [лайк, линк на фото максимального размера, размер]
        """
        URL = 'https://api.vk.com/method/photos.getAll'
        params = {
            'owner_id': self.owner_id,
            'extended': 1,
            'count': f'{self.count_for_download}',
            'access_token': self.token_vk,
            'v': '5.331'
        }

        list_photo = []  # список [лайки, линк, размер]

        req = requests.get(URL, params).json()
        req = req['response']['items']

        # перебираем все доступные фотографии
        # likes - количество лайков у фотографии
        # sizes - доступные размеры фотографии (словарь)
        for photo_vk in req:
            likes = photo_vk['likes']['count']
            sizes = photo_vk['sizes']
            sizes_set = set()

            #  получаем сет из всех доступных размеров фотографий
            for s in sizes:
                sizes_set.add(s['type'])

            # добавляем ссылку на самую большую фотографию в list_photo
            if 'w' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'w':  # линк на размер фото
                        list_photo.append([likes, lnk['url'], lnk['type']])  # + список [лайки, линк, размер]
                        break
            elif 'z' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'z':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break
            elif 'y' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'y':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break
            elif 'r' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'r':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break
            elif 'q' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'q':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break
            elif 'p' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'p':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break
            elif 'o' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'o':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break
            elif 'x' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'x':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break
            elif 'm' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 'm':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break
            elif 's' in sizes_set:
                for lnk in sizes:
                    if lnk['type'] == 's':
                        list_photo.append([likes, lnk['url'], lnk['type']])
                        break

        return list_photo
