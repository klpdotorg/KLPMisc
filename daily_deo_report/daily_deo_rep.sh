cd /home/klp/ems-production
echo 'Removing yesterdays and weekend old report ' $(date --date="1 days ago" +%Y%m%d)
rm -rf logFiles/deoreportquery-$(date --date="1 days ago" +%Y%m%d).csv
rm -rf logFiles/deoreportquery-$(date --date="3 days ago" +%Y%m%d).csv
echo 'Start of DEOHistory process'
python manage.py KLP_DEOHistoryquery $(date +%d/%m/%Y) $(date +%d/%m/%Y) deoreportquery-$(date +%Y%m%d)
echo 'End of DEOHistory process'
../daily_deo_report/daily_deo_rep.py logFiles/deoreportquery-$(date +%Y%m%d).csv
echo ' Sent mail and exit'
cd ~
