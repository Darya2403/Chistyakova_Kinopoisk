import requests
from neo4j import GraphDatabase

def genres_countries(session):
    #Получаем жанры и страны
    response = requests.get('https://kinopoiskapiunofficial.tech/api/v2.2/films/filters',
                            headers={'X-API-KEY': 'eaf99c7a-23ee-4d61-918c-e683a457ba98', 'Content-Type': 'application/json'})
    #Проверяем, что получили
    if response.status_code == 200:
         try:
            data = response.json()
            print(data)
         except ValueError:
            print("В ответе не JSON")
    else:
        print("Error: ", response.status_code)

    #Создаем узлы стран
    for country in data['countries']:
        session.run("MERGE (:Country {name: $name, id: $id})", name=country['country'], id=country['id'])

    #Создаем узлы жанров
    for genre in data['genres']:
        session.run("MERGE (:Genre {name: $name, id: $id})", name=genre['genre'], id=genre['id'])