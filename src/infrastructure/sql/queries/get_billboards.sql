SELECT 
    b.*,
    ol.date_begin,
    ol.date_end
FROM 
    billboards b
JOIN 
    order_lines ol ON b.id = ol.billboard_id
JOIN 
    orders o ON ol.order_id = o.id
JOIN 
    external_users u ON o.tenant_id = u.id
WHERE 
    u.lastname LIKE '$lastname%'
    AND MONTH(o.registration_date) = $month 
    AND YEAR(o.registration_date) = $year
ORDER BY 
    b.city, b.cost;