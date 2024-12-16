IF EXISTS(SELECT * from 'billboard_report_$year_$month')
ELSE SELECT 0;