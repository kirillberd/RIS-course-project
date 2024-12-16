SELECT * 
FROM information_schema.tables
WHERE table_schema = 'billboards' 
    AND table_name = '$table_name'
LIMIT 1;