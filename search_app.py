import sys
from io import BytesIO
import requests
from PIL import Image
from data_snippet import create_data_snippet, pprint_data_snippet

toponym_to_find = " ".join(sys.argv[1:])

try:
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                       "geocode": toponym_to_find, "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params).json()
    toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    lon, lat = toponym["Point"]["pos"].split()

    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {"apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3", "text": "аптека",
                     "lang": "ru_RU", "ll": ','.join([lon, lat]), "type": "biz"}
    response = requests.get(search_api_server, params=search_params).json()

    marks = list()
    for i in range(min(len(response["features"]), 10)):
        organization = response["features"][i]
        pprint_data_snippet(create_data_snippet(organization, [lon, lat]))
        point = organization["geometry"]["coordinates"]
        try:
            if "TwentyFourHours" in organization["properties"]["CompanyMetaData"]["Hours"]["Availabilities"][0]:
                style = "pm2dgl"
            else:
                style = "pm2bll"
        except KeyError:
            style = "pm2grl"
        marks.append("{0},{1},{2}".format(point[0], point[1], style))

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {"ll": ','.join([lon, lat]), "l": "map", "pt": '~'.join(marks)}
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()

except Exception:
    print("Возникла ошибка при работе с API!")
    sys.exit()
