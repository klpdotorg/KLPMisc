#!/usr/bin/env python
import os,sys
import datetime
from datetime import date
import traceback
import csv
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from Utility import KLPDB

def summarize(datafile,cursor):
  csvbuffer = csv.reader(open(datafile,'r'), delimiter=',')
  header = csvbuffer.next()
  preschdata = [] 
  schdata = [] 
  assessments = {}
  for row in csvbuffer:
    preschdata.append( {"User" : row[1],
                  "School-C" : row[8],
                  "School-U" : row[9],
                  "School-D" : row[10],
                  "Student-C" : row[14],
                  "Student-U" : row[15],
                  "Student-D" : row[16],
                  "Staff-C" : row[20],
                  "Staff-U" : row[21],
                  "Staff-D" : row[22] })
    schdata.append({"User" : row[1],
                  "School-C" : row[11],
                  "School-U" : row[12],
                  "School-D" : row[13],
                  "Student-C" : row[17],
                  "Student-U" : row[18],
                  "Student-D" : row[19],
                  "Staff-C" : row[23],
                  "Staff-U" : row[24],
                  "Staff-D" : row[25] })
    rowlen = len(row)
    for i in range(26,rowlen):
      if header[i] == "Assess Id":
        assess = getAssessmentData(row[i],cursor)
        pgm_head = assess[0] 
        if pgm_head not in assessments.keys():
          assessments[pgm_head] ={}
        assess_head = assess[1] + "; Type:" + assess[2] + "; No.of Questions:" + str(assess[3])
        if assess_head not in assessments[pgm_head].keys():
          assessments[pgm_head][assess_head] ={}
        tot_entries = long(row[i+1]) + long(row[i+2]) + long(row[i+3]) + long(row[i+4])
        if tot_entries > 0:
          assessments[pgm_head][assess_head][row[1]]={"Correct": long(row[i+1])/assess[3],
                                     "Incorrect": long(row[i+2])/assess[3],
			             "Verified": long(row[i+3])/assess[3],
			             "Rectified": long(row[i+4])/assess[3]}
  headers = ['User','Student-C','Student-U','Student-D','School-C','School-U','School-D','Staff-C','Staff-U','Staff-D']
  wf = open("summary_file.csv",'w')
  wf.write("PRESCHOOL DATA SUMMARY\n")
  wf.write('|'.join(headers)+'\n')
  for each in preschdata:
    newline = ""
    if sum(map(int,each.values()[2:])) + int(each.values()[0])> 0:
      for i in headers:
        newline = newline + each[i]+'|'
      wf.write(newline.lstrip('|') + '\n')
  wf.write("\nSCHOOL DATA SUMMARY\n")
  wf.write('|'.join(headers)+'\n')
  for each in schdata:
    newline = ""
    if sum(map(int,each.values()[2:])) + int(each.values()[0])> 0:
      for i in headers:
        newline = newline + each[i]+'|'
      wf.write(newline.lstrip('|') + '\n')
  wf.write("\nASSESSMENT SUMMARY\n")
  for pgm in assessments.keys():
    wf.write("\n"+pgm+"\n")
    for key in assessments[pgm]:
      wf.write("\n"+key+"\n")
      wf.write("User|Correct|Incorrect|Verified|Rectified\n")
      details = assessments[pgm][key]
      for each in details.keys():
        wf.write(each + '|' + str(details[each]["Correct"]) 
                    + '|' + str(details[each]["Incorrect"]) 
                    + '|' + str(details[each]["Verified"]) 
                    + '|' + str(details[each]["Rectified"]) + '\n')

def getAssessmentData(assessid,cursor):
  details = []
  cursor.execute("select p.name,a.name,case a.typ when 1 then 'school' when 2 then 'class' else 'student' end,count(q.id) from schools_assessment a,schools_programme p,schools_question q where a.programme_id = p.id and q.assessment_id = a.id and a.id =%s and q.active=2 group by p.name,a.name,a.typ;",(assessid,))
  result = cursor.fetchall()
  for row in result:
    details = row
  return details
    
def mail(sub,textstr,filenamestr,filedir,summary_file):
  subject = sub
  from ConfigParser import SafeConfigParser
  config = SafeConfigParser()
  #Path is /home/klp/production when the script execution comes here
  config.read('../daily_deo_report/config/monthly_config.ini')
  sender = config.get('Mail','senderid')
  senderpwd = config.get('Mail','senderpwd')
  cc = config.get('Mail','cc_ids').split(',')
  to = config.get('Mail','to_ids').split(',')
  smtpport = config.get('Mail','smtpport')
  smtpserver = config.get('Mail','smtpserver')

  # create html email
  html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
  html +='"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">'
  html +='<body style="font-size:14px;font-family:Verdana"><p>'+textstr+'</p>'
  html += "</body></html>"
  emailMsg = MIMEMultipart()
  emailMsg['Subject'] = subject
  emailMsg['From'] = sender 
  emailMsg['To'] = ', '.join(to)
  emailMsg['Cc'] = ", ".join(cc)
  emailMsg.attach(MIMEText(html,'html'))
  fileMsg = MIMEBase('application', "octet-stream")
  fileMsg.set_payload(open(filenamestr,'rb').read())
  Encoders.encode_base64(fileMsg)
  fileMsg.add_header('Content-Disposition','attachment;filename='+filenamestr.lstrip(filedir))
  emailMsg.attach(fileMsg)
  fileMsg = MIMEBase('application', "octet-stream")
  fileMsg.set_payload(open(summary_file,'rb').read())
  Encoders.encode_base64(fileMsg)
  fileMsg.add_header('Content-Disposition','attachment;filename='+summary_file.split('/')[summary_file.count('/')])
  emailMsg.attach(fileMsg)

  # send email
  server = smtplib.SMTP(smtpserver,smtpport)
  server.ehlo()
  server.starttls()
  server.ehlo
  server.login(sender,senderpwd)
  server.sendmail(sender,to+cc,emailMsg.as_string())
  server.close()

#-------------------MAIN BEGINS

thisday = date.today()
lastmonth = thisday - datetime.timedelta(days=30)
startdatestr = '21/'+str(lastmonth.month)+'/'+str(lastmonth.year)
enddatestr = '20/'+str(thisday.month)+'/'+str(thisday.year)
reportfile = sys.argv[1]

try:
  cursor = KLPDB.getConnection().cursor()
  summarize(os.getcwd() + '/' + reportfile,cursor)
  emailtext = 'Please find Report attached for Start date:' + startdatestr + ' - End date:' + enddatestr
  mail('[EMS-E2E] Monthly DEO Report generated for the date:' + startdatestr, emailtext,reportfile,'logFiles/','/home/klp/daily_deo_report/summary_file.csv')
except:
  print "Unexpected error:", sys.exc_info()
  print "Exception in user code:"
  print '-'*60
  traceback.print_exc(file=sys.stdout)
  print '-'*60
finally:
  pass
