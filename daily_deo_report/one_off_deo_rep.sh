#!/bin/sh

#While using this script, make sure you change the date ranges appropriately
cd /home/klp/ems-production
echo 'Start of DEOHistory process'
python manage.py  KLP_DEOHistoryquery 21/07/2013 20/08/2013 oneoff_report_2107_to_2008
echo 'End of DEOHistory process'
sleep 600
../daily_deo_report/one_off_deo_rep.py logFiles/oneoff_report_2107_to_2008.csv '21/07/2013-20/08/2013'
echo ' Sent mail and exit'
cd ~
