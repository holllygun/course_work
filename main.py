import requests
from tqdm import tqdm
import json
from pprint import pprint
import time


class VK:
    def __init__(self, token, vkid, yandex):
        self.token = token
        self.vkid = vkid
        self.yandex = yandex

    def get_photos(self):
        params = {"owner_id": self.vkid, "access_token": self.token, "album_id": "profile", "v": 5.103, "offset": 0, "photo_sizes": 0, "count": 5, "extended": 1, "rev": 1}
        api = requests.get("https://api.vk.com/method/photos.get", params=params).json()
        p_list = []
        for item in api['response']['items']:
             photo = max([size['height'] for size in item['sizes']])
             name = f"{item['likes']['count']}.jpg"
             for size in item['sizes']:
                 if size['height'] == photo:
                     size["file_name"] = name
                     p_list.append(size)

        y_url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": "VK_photos"}
        headers = {"Authorization": self.yandex}
        response = requests.put(y_url, headers=headers, params=params)
        url_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for p in p_list:
            name = p["file_name"]
            url = p["url"]
            params = {"path": "/VK_photos/" + name, "url": url}
            requests.post(url_upload, params=params, headers=headers)
        with open("json_data", "w") as f:
            json.dump(p_list, f)
        pbar = tqdm(p_list, colour="green", )
        for p in pbar:
            time.sleep(1)
        print("Все загрузилось! Ура!")

vktoken = "..."
vk_id = input("Введите ваш VK id: ")
yandex_token = input("Введите ваш Yandex-токен: ")
uploader = VK(vktoken, vk_id, yandex_token)
res = uploader.get_photos()



