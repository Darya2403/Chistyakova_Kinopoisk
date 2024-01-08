from neo4j import GraphDatabase
import requests
import Genres_countries
#import Constraints
import Films_staff

#Соединяемся с Neo4J
uri = "neo4j+s://70cea92a.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "0R9vKtBZ_bLLdNrmaZBbqwH1xSvNsOsmGtsIyqp2zgQ"))

with driver.session() as session:
    #Вызываем функцию по заполнению жанров и стран, достаточно однократного запуска
    Genres_countries.genres_countries(session)
    #Вызываем функцию по созданию ограничений, однократный запуск, закомментирована
    #Constraints.constraints(session)
    #Вызываем функцию по заполнению фильмов и сотрудников
    Films_staff.films_staff(session)

driver.close()