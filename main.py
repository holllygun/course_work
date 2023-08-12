import requests
from tqdm import tqdm
import json
from pprint import pprint
import time
from datetime import datetime, date


class VK:
    def __init__(self, token, vkid, yandex):
        self.token = token
        self.vkid = vkid
        self.yandex = yandex

    def get_photos(self):
        params = {"owner_id": self.vkid, "access_token": self.token, "album_id": "profile", "v": 5.103, "offset": 0, "photo_sizes": 0, "count": 5, "extended": 1, "rev": 1}
        api = requests.get("https://api.vk.com/method/photos.get", params=params).json()
        return api

    def make_list(self, api: dict):
        p_list = []
        a = set()
        for item in api['response']['items']:
            d = date.fromtimestamp(item["date"])
            dateofpost = f"{d}.jpg"
            photo = max([size['height'] for size in item['sizes']])
            like = item['likes']['count']
            for size in item['sizes']:
                if size['height'] == photo:
                    if like in a:
                        size["file_name"] = dateofpost
                        p_list.append(size)
                        break
                    else:
                        size["file_name"] = f"{like}.jpg"
                        a.add(like)
                        p_list.append(size)
        return p_list

    def upload_photo(self, p_list):
        from tqdm import tqdm
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

    def get_json(self, p_list):
        with open("json_data", "w") as f:
            json.dump(p_list, f)

    def progress_bar(self, p_list):
        pbar = tqdm(p_list, colour="green",)
        for p in pbar:
            time.sleep(1)
        print("Все загрузилось! Ура!")

    def final_result(self):
        api = uploader.get_photos()
        p_list = uploader.make_list(api)
        uploader.upload_photo(p_list)
        uploader.get_json(p_list)
        uploader.progress_bar(p_list)



vktoken = "..."
vk_id = input(" Введите ваш vk id")
yandex_token = input("Введите ваш Yandex-токен: ")
uploader = VK(vktoken, vk_id, yandex_token)
uploader.final_result()


