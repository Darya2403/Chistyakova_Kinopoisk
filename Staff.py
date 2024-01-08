import requests

def staff(session, film):
    #Делаем запрос по каждому фильму для получения всех сотрудников
    response2 = requests.get('https://kinopoiskapiunofficial.tech/api/v1/staff',
                             params={"filmId": film['kinopoiskId']},
                             headers={'X-API-KEY': 'eaf99c7a-23ee-4d61-918c-e683a457ba98',
                                      'Content-Type': 'application/json'})
    #Проверяем, что получили
    if response2.status_code == 200:
        try:
            data2 = response2.json()
            for staff in data2:
                #Создаем узел сотрудник + где необходимо, проверки на none
                name = staff['nameEn']
                russian_name = staff['nameRu']
                staffId = staff['staffId']
                if staff['posterUrl'] is not None:
                   posterUrl = staff['posterUrl']
                else:
                   posterUrl = 'no inf'
                #Создаем узел сотрудник
                session.run("MERGE (s:Staff {name: $name, russian_name: $russian_name, staffId: $staffId, posterUrl: $posterUrl})",
                            name=name,
                            russian_name=russian_name,
                            staffId=staffId,
                            posterUrl=posterUrl)
                #Создаем связь сотрудник-фильм
                relationship = staff['professionKey']
                session.run("MATCH (f:Film {kinopoiskId: $kinopoiskId}), (s:Staff {name: $name}) MERGE (f)-[:"+relationship+"]->(s)",
                            name=staff['nameEn'], kinopoiskId=film['kinopoiskId'])

        except ValueError:
            print("В ответе не JSON")
    else:
        print("Error: ", response2.status_code)