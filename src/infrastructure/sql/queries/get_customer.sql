SELECT 
   u.*,
   COUNT(DISTINCT o.id) as orders_count,
   SUM(o.total_cost) as total_sum,
   GROUP_CONCAT(
       DISTINCT CONCAT(
           b.id, ' (', 
           b.city, ', ', 
           b.addres, ')'
       ) 
       SEPARATOR '; '
   ) as billboards
FROM 
   external_users u
JOIN 
   orders o ON u.id = o.tenant_id
JOIN 
   order_lines ol ON o.id = ol.order_id
JOIN 
   billboards b ON ol.billboard_id = b.id
WHERE 
   MONTH(o.registration_date) = $month 
   AND YEAR(o.registration_date) = $year
GROUP BY 
   u.id, u.firstname, u.lastname, u.username, u.phone, u.password, u.role
ORDER BY 
   total_sum DESC, orders_count DESC;