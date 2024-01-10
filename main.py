from neo4j import GraphDatabase
import Genres_countries
#import Constraints
import Films_staff

#Соединяемся с Neo4J
uri = "neo4j+s://70cea92a.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "0R9vKtBZ_bLLdNrmaZBbqwH1xSvNsOsmGtsIyqp2zgQ"))
#Доступ к АПИ кинопоиска
password = 'eaf99c7a-23ee-4d61-918c-e683a457ba98'

#Вызываем функцию по созданию ограничений, однократный запуск, закомментирована
#Constraints.constraints(driver)
#Вызываем функцию по заполнению жанров и стран, достаточно однократного запуска
Genres_countries.genres_countries(driver, password)
#Вызываем функцию по заполнению фильмов и сотрудников
Films_staff.films_staff(driver, password)
