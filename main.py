import vkapi
import yaapi
import json

if __name__ == "__main__":
    # Либо screen_name, либо owner_id
    vk_api = vkapi.VkApi(count_for_download=5, screen_name="abcde")
    ya_api = yaapi.YaApi()
    count_progress = 1  # счетчик прогресса

    # Обрабатываем (копируем) каждое фото по отдельности из списка vk_api.get_photos()
    for photo in vk_api.get_photos():
        print(f'Обрабатывается фото {count_progress} из {vk_api.count_for_download}')
        ya_api.upload_ya(photo)
        count_progress += 1

    # список фотографий в json формате, создается photos.json
    with open("photos.json", "w") as outfile:
        json.dump(ya_api.photos, outfile)
