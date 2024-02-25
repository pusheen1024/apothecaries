from distance import distance


def create_data_snippet(organization, point):
    data = dict()
    data["Название аптеки"] = organization["properties"]["name"]
    data["Адрес аптеки"] = organization["properties"]["CompanyMetaData"]["address"]
    try:
        data["Время работы аптеки"] = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    except KeyError:
        pass
    point_1 = tuple(map(float, point))
    point_2 = organization["geometry"]["coordinates"]
    data["Расстояние до исходного местоположения"] = f"{distance(point_1, point_2):.2f} метров"
    return data


def pprint_data_snippet(dictionary):
    for key, value in dictionary.items():
        print(f'{key} - {value}')
