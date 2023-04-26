import requests
from datetime import datetime
import json

# токен вконтакте из файла token_vk.txt
with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()

# токен яндекс из файла token_ya.txt
with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()


def get_photos():
    """
    Получение списка фотографий вк
    :return: список [лайк, линк на фото максимального размера, размер]
    """
    URL = 'https://api.vk.com/method/photos.getAll'
    params = {
        'owner_id': owner_id,
        'extended': 1,
        'count': f'{count_for_download}',
        'access_token': token_vk,
        'v': '5.331'
    }

    list_photo = []  # список [лайки, линк, размер]

    req = requests.get(URL, params).json()
    req = req['response']['items']

    # перебираем все доступные фотографии
    # likes - количество лайков у фотографии
    # sizes - доступные размеры фотографии (словарь)
    for photo in req:
        likes = photo['likes']['count']
        sizes = photo['sizes']
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


def get_headers_ya():
    """
    Получение заголовка Яндекс Диск
    """
    return {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {token_ya}'
    }


def make_dir_ya(dir_name):
    """
    Создание каталога на Яндекс Диске
    :param dir_name: название папки
    """
    URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = get_headers_ya()
    params = {
        'path': f'/{dir_name}'
    }
    requests.put(URL, headers=headers, params=params).json()


def get_upload_link_ya(likes, size, directory='backup', exist=False):
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
        for i in photos:
            if i['file_name'] == f'{directory}/{likes}.jpg':
                photos.remove(i)
    else:  # если файл не существует
        name_of_file = f'{directory}/{likes}.jpg'

    # создаем каталог для копий фотографий в Яндекс Диске
    make_dir_ya(directory)

    URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = get_headers_ya()
    params = {
        'path': f'{name_of_file}',
        'overwrite': 'false'
    }
    req = requests.get(URL, headers=headers, params=params).json()

    photos.append({'file_name': name_of_file, 'size': size})

    return req['href']


def upload_ya(photos):
    """
    Загружаем фото на Яндекс Диск
    :param photos: список get_photos(), [0] - лайки, [1] - линк на фото
    """
    url = photos[1]
    data = requests.get(url)
    try:  # если файл не существует
        requests.put(url=get_upload_link_ya(likes=photos[0], size=photos[2]), data=data)
    except Exception:  # если файл существует (добавляется параметр exist=True)
        requests.put(url=get_upload_link_ya(likes=photos[0], size=photos[2], exist=True), data=data)


owner_id = 1  # id пользователя вконтакте
count_for_download = 5  # количество фото для загрузки

list_photos = get_photos()
count_progress = 1  # счетчик прогресса
file_name = ''  # имя файла на яндекс диске
photos = []  # список фотографий для json дампа

for photo in list_photos:
    print(f'Обрабатывается фото {count_progress} из {count_for_download}')
    upload_ya(photo)
    count_progress += 1

# список фотографий в json формате, создается photos.json
with open("photos.json", "w") as outfile:
    json.dump(photos, outfile)
