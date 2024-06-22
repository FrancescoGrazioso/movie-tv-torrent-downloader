import json


class ConfigManager:
    QBITTORRENT_AUTH = None
    QBITTORRENT_URL = None
    QBITTORRENT_SAVE_PATH = None

    def __init__(self):
        self.__get_qbittorrent_auth()
        self.__get_qbittorrent_url()
        self.__get_qbittorrent_save_path()

    def __get_qbittorrent_auth(self):
        with open("config.json") as f:
            data = json.load(f)
        self.QBITTORRENT_AUTH = data["AUTH"]["QB_USER"], data["AUTH"]["QB_PASSWD"]

    def __get_qbittorrent_url(self):
        with open("config.json") as f:
            data = json.load(f)
        self.QBITTORRENT_URL = data["QB_URL"]

    def __get_qbittorrent_save_path(self):
        with open("config.json") as f:
            data = json.load(f)
        self.QB_DEFAULT_SAVE_PATH = data["QB_DEFAULT_SAVE_PATH"]
