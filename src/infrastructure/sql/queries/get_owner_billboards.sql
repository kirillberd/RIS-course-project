SELECT *
FROM billboards
WHERE 1=1
$owner_clause
$city_clause
$quality_clause
ORDER BY city, cost;