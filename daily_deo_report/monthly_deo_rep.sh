#!/bin/sh

year=$(date +%Y)
month=$(date +%m)
month=`echo $month | awk '{printf( "%d", $1 )}'`
lastmonth=$(($month-1))
lastyear=$(($year))
if [ $month -eq 1 ]; then
        lastyear=$(($year-1))
        lastmonth=12
fi
cd /home/klp/ems-production
echo 'Start of DEOHistory process'
python manage.py  KLP_DEOHistoryquery 21/$lastmonth/$lastyear 20/$month/$year monthly_query_report-$(date +%B%Y)
#python manage.py  KLP_DE_activity_report_sep 21/$lastmonth/$lastyear 20/$month/$year monthly_report-$(date +%B%Y)
echo 'End of DEOHistory process'
../daily_deo_report/monthly_deo_rep.py logFiles/monthly_query_report-$(date +%B%Y).csv
#../daily_deo_report/monthly_deo_rep.py logFiles/monthly_report-$(date +%B%Y).csv
echo ' Sent mail and exit'
cd ~
