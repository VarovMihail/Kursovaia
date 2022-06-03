import json
import sys
import requests
from pprint import pprint
from tqdm import tqdm


class Ya_loader:

    def __init__(self,id_vk,token_vk,token_yd):
        self.id_vk = id_vk
        self.token_vk = token_vk
        self.token_yd = token_yd


    #создание папки
    def make_folder(self,name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.name = name
        params = {'path': self.name, 'overwrite': True}
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_yd}'}
        response = requests.put(url, params = params, headers = headers)

    #получение фото из Контакта
    def get_photo(self):
        URL = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': id_vk,'album_id':'profile','photo_sizes':'1','extended':'1','access_token': token_vk, 'v':'5.131'}
        res = requests.get(URL,params = params)
        data = res.json()
        #pprint(data)

        self.ldict = []
        for i in data['response']["items"]:
            dict = {}
            dict["file_name"] = str(i['likes']['count']) + str(i['date']) + '.jpg'
            dict["link"] = i['sizes'][-1]["url"]
            dict["size"] = i['sizes'][-1]['type']
            self.ldict.append(dict)
        #запись данных в файл
        with open('new.json','w') as new:
            json.dump(self.ldict,new,indent=2)

    # загрузка фото на Яндекс Диск
    def load_photo(self):
        with tqdm(total=100) as pbar:
            for dict in self.ldict:
                pbar.update(100/len(self.ldict))
                # получение ссылки на загрузку
                url = f'https://cloud-api.yandex.net/v1/disk/resources/upload/'
                path_to_file = f'papka/{dict["file_name"]}'
                photo = requests.get(dict["link"])
                params = {'path': path_to_file, 'overwrite': True}
                headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_yd}'}
                response = requests.get(url, params=params, headers=headers)
                upload_link = response.json()['href']
                # загрузка фотографии
                res = requests.put(upload_link, data=photo)
                #print(res.status_code)

id_vk = input('Введите id_vk: ')
token_vk = input('Введите token_vk: ')
token_yd = input('Введите token_yd: ')

a = Ya_loader(id_vk,token_vk,token_yd)
a.make_folder('papka')
a.get_photo()
a.load_photo()






