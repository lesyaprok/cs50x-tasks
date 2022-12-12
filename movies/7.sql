SELECT movies.title as title, ratings.rating as rating
FROM movies
JOIN ratings
ON ratings.movie_id = movies.id
WHERE movies.year = 2010
ORDER BY rating DESC, movies.title ASC