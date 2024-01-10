import requests
import time

def staff(session, password, film):
    #Делаем запрос по каждому фильму для получения всех сотрудников
    response2 = requests.get('https://kinopoiskapiunofficial.tech/api/v1/staff',
                             params={"filmId": film['kinopoiskId']},
                             headers={'X-API-KEY': password,
                                      'Content-Type': 'application/json'})
    #Проверяем, что получили
    if response2.status_code == 200:
        try:
            data2 = response2.json()
            for staff in data2:
                #Создаем узел сотрудник + где необходимо, проверки на none
                if staff['nameEn'] is not None:
                    name = staff['nameEn']
                else:
                    name = 'no inf'
                if staff['nameRu'] is not None:
                    russian_name = staff['nameRu']
                else:
                    russian_name = 'no inf'
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
                session.run("MATCH (f:Film {kinopoiskId: $kinopoiskId}), (s:Staff {staffId: $staffId}) MERGE (f)-[:"+relationship+"]->(s)",
                            staffId=staff['staffId'], kinopoiskId=film['kinopoiskId'])
            time.sleep(0.05)
        except ValueError:
            print("Ошибка формата: ", data2)
    else:
        print("Error: ", response2.status_code)