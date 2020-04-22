select avg(ratings.rating)
from ratings
INNER JOIN movies ON ratings.movie_id = movies.id
where movies.year = 2012;