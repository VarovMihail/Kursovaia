import json
import sys
import requests
from pprint import pprint
from tqdm import tqdm

id_vk = input('id пользователя ВК: ')
token_vk = input('введите ключ ВК: ')
token_yd = input('введите ключ Яндекс: ')


#создание папки
url = 'https://cloud-api.yandex.net/v1/disk/resources/'
name = 'papka'
params = {'path': name, 'overwrite': True}
headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_yd}'}
response = requests.put(url, params = params, headers = headers)

#получение фото из Контакта
URL = 'https://api.vk.com/method/photos.get'
params = {'owner_id': id_vk,'album_id':'profile','photo_sizes':'1','extended':'1','access_token': token_vk, 'v':'5.131'}
res = requests.get(URL,params = params)
data = res.json()
#pprint(data)

ldict = []
for i in data['response']["items"]:
    dict = {}
    dict["file_name"] = str(i['likes']['count']) + str(i['date']) + '.jpg'
    dict["link"] = i['sizes'][-1]["url"]
    dict["size"] = i['sizes'][-1]['type']
    ldict.append(dict)
#pprint(ldict)

#запись данных в файл
with open('new.json','w') as new:
    json.dump(ldict,new,indent=2)
#sys.exit()
#загрузка фото на Яндекс Диск
with tqdm(total=100) as pbar:
    for dict in ldict:
        pbar.update(100/len(ldict))
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













