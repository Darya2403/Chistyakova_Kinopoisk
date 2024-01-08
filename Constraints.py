from neo4j import GraphDatabase

def constraints(session):
    #Создаем ограничения уникальности на БД
    session.run("CREATE CONSTRAINT FOR (f:Film) REQUIRE f.kinopoiskId IS UNIQUE")
    session.run("CREATE CONSTRAINT FOR (g:Genre) REQUIRE g.id IS UNIQUE")
    session.run("CREATE CONSTRAINT FOR (c:Country) REQUIRE c.id IS UNIQUE")
    session.run("CREATE CONSTRAINT FOR (s:Staff) REQUIRE s.staffId IS UNIQUE")