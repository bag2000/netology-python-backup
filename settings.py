import configparser


class Settings:
    """
    Класс для работы с настройками
    """
    config = configparser.ConfigParser()
    config.read("settings.ini")

    def get_token_vk(self):
        """
        Получение токена вконтакте
        :return: токен вконтакте
        """
        return self.config["VK"]["token"]

    def get_token_ya(self):
        """
        Получение токена яндекс диск
        :return: токен яндекс диска
        """
        return self.config["YA"]["token"]
