import requests
import Staff
import time
def films_staff(driver, password):
    #Обработка ошибки соединения с neo4j
    try:
        with driver.session() as session:
            #Список жанров и стран из БД
            results = session.run("MATCH (g:Genre), (c:Country) RETURN g.id, c.id ORDER BY id(g), id(c)")
            #Задаем стартовые значения id для перебора
            start_genre_id = 1
            start_country_id = 1

            #Цикл по перебору всех вариаций жанра и стран
            for genre, country in results:
                #Проверка на стартовые значения
                if genre >= start_genre_id and country >= start_country_id:
                    print('Жанр: ', genre, ', страна: ', country)
                    #Получаем фильмы в цикле по странице с передачей страны и жанра
                    page = 1
                    total_pages = 1
                    while page <= total_pages:
                        response = requests.get('https://kinopoiskapiunofficial.tech/api/v2.2/films', params={"countries": country, "genres": genre, "page": page},
                                                headers={'X-API-KEY': password, 'Content-Type': 'application/json'})
                        #Проверяем, что получили
                        if response.status_code == 200:
                            try:
                                data = response.json()
                                #print(data)
                                total_pages = data["totalPages"]
                                page += 1
                                #Перечисляем параметры + где необходимо, проверки на none
                                for film in data['items']:
                                    name = film['nameOriginal']
                                    kinopoiskId = film['kinopoiskId']
                                    if film['imdbId'] is not None:
                                        imdbId = film['imdbId']
                                    else:
                                        imdbId = 'no inf'
                                    if film['ratingKinopoisk'] is not None:
                                        ratingKinopoisk = film['ratingKinopoisk']
                                    else:
                                        ratingKinopoisk = 'no inf'
                                    if film['ratingImdb'] is not None:
                                        ratingImdb = film['ratingImdb']
                                    else:
                                        ratingImdb = 'no inf'
                                    if film['year'] is not None:
                                        year = film['year']
                                    else:
                                        year = 'no inf'
                                    if film['type'] is not None:
                                        type = film['type']
                                    else:
                                        type = 'no inf'
                                    #Создаем узел фильма
                                    session.run("MERGE (f:Film {name: $name, kinopoiskId: $kinopoiskId, imdbId: $imdbId, ratingKinopoisk: $ratingKinopoisk, ratingImdb: $ratingImdb, year: $year, type: $type})",
                                                name=name,
                                                kinopoiskId=kinopoiskId,
                                                imdbId=imdbId,
                                                ratingKinopoisk=ratingKinopoisk,
                                                ratingImdb=ratingImdb,
                                                year=year,
                                                type=type)
                                    #Создаем связь фильм-страна
                                    session.run("MATCH (f:Film {kinopoiskId: $kinopoiskId}), (c:Country {id: $id}) MERGE (f)-[:FILMED_IN]->(c)",
                                                id=country, kinopoiskId=film['kinopoiskId'])
                                    #Создаем связь фильм-жанр
                                    session.run("MATCH (f:Film {kinopoiskId: $kinopoiskId}), (g:Genre {id: $id}) MERGE (f)-[:BELONGS_TO]->(g)",
                                                id=genre, kinopoiskId=film['kinopoiskId'])

                                    #Вызываем функцию запроса сотрудников по каждому фильму
                                    Staff.staff(session, password, film)
                                time.sleep(0.05)
                            except ValueError:
                                print("Ошибка формата: ", data)
                        else:
                            print("Error: ", response.status_code)
                else:
                    print('Жанр', genre, 'и страна', country, 'не входят в заданный диапазон')
    except OSError as e:
        print("Ошибка соединения с Neo4j:", e, 'Остановка на жанре: ', genre, ', стране: ', country)
    finally:
        if driver is not None:
            driver.close()
