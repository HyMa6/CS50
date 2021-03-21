SELECT name, COUNT(name) FROM people where id IN
    (SELECT person_id FROM stars WHERE movie_id IN
        (SELECT movie_id FROM stars WHERE person_id =
            (SELECT id FROM people WHERE name = "Kevin Bacon" AND birth = 1958 )))
AND id !=
    (SELECT id FROM people WHERE name = "Kevin Bacon" AND birth = 1958)