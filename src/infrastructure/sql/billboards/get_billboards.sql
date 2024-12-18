SELECT b.* 
FROM billboards b
WHERE 1=1
$schedule_clause
$city_clause
$direction_clause
$cost_min_clause
$cost_max_clause
$size_min_clause
$size_max_clause
$quality_clause
$address_clause
ORDER BY b.city, b.cost;