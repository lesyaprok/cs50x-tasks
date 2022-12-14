SELECT title FROM movies
WHERE id in (SELECT movie_id FROM stars
WHERE person_id in (SELECT id FROM people
WHERE (name = "Johnny Depp" or name = "Helena Bonham Carter"))
GROUP BY movie_id
HAVING COUNT(movie_id) > 1)