def constraints(driver):
    try:
        with driver.session() as session:
            #Создаем ограничения уникальности на БД
            session.run("CREATE CONSTRAINT FOR (f:Film) REQUIRE f.kinopoiskId IS UNIQUE")
            session.run("CREATE CONSTRAINT FOR (g:Genre) REQUIRE g.id IS UNIQUE")
            session.run("CREATE CONSTRAINT FOR (c:Country) REQUIRE c.id IS UNIQUE")
            session.run("CREATE CONSTRAINT FOR (s:Staff) REQUIRE s.staffId IS UNIQUE")
    except OSError as e:
        print("Ошибка соединения с Neo4j:", e)
    finally:
        if driver is not None:
            driver.close()