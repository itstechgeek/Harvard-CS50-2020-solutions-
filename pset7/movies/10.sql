select distinct name
from people
where id in (select person_id from directors where id in (select movie_id from ratings where rating >= 9));