SELECT * FROM billboards 
WHERE 1=1
{city_clause}
{direction_clause}
{cost_min_clause}
{cost_max_clause}
{size_min_clause}
{size_max_clause}
{quality_clause}
{address_clause}
{date_from_clause}
{date_to_clause}
ORDER BY city, cost;

