import requests

def genres_countries(driver, password):
    #Обработка ошибки соединения с neo4j
    try:
        with driver.session() as session:
            #Получаем жанры и страны
            response = requests.get('https://kinopoiskapiunofficial.tech/api/v2.2/films/filters',
                                    headers={'X-API-KEY': password, 'Content-Type': 'application/json'})
            #Проверяем, что получили
            if response.status_code == 200:
                 try:
                    data = response.json()
                    print(data)
                    # Создаем узлы стран
                    for country in data['countries']:
                        session.run("MERGE (:Country {name: $name, id: $id})", name=country['country'],
                                    id=country['id'])
                    # Создаем узлы жанров
                    for genre in data['genres']:
                        session.run("MERGE (:Genre {name: $name, id: $id})", name=genre['genre'], id=genre['id'])
                 except ValueError:
                    print("Ошибка формата: ", data)
            else:
                print("Error: ", response.status_code)
    except OSError as e:
        print("Ошибка соединения с Neo4j:", e)
    finally:
        if driver is not None:
            driver.close()