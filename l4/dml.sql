set search_path to stackoverflow_filtered;

-- How many cities appeared more than twice in your results table?
select COUNT(city) from results HAVING
   COUNT (city) > 2;

-- (0 rows)


-- How many unique created_at dates(not datetime) are in the result table?


-- If you were to give an award to one user, who will it be? And why?



