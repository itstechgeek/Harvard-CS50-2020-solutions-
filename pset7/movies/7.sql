select movies.title , ratings.rating from movies
INNER JOIN ratings ON movies.id = ratings.movie_id
where movies.year = 2010
order by ratings.rating DESC , title ASC;