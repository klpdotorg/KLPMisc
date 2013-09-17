#!/usr/bin/env python
import os,sys
import datetime
from datetime import date
import traceback
#import smtplib,email,email.encoders,email.mime.text,email.mime.base,mimetypes
import csv
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def mail(sub,textstr,filenamestr,filedir):
  subject = sub
  from ConfigParser import SafeConfigParser
  config = SafeConfigParser()
  #Path is /home/klp/production when the script execution comes here
  config.read('../daily_deo_report/config/daily_config.ini')
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
  #emailMsg = email.MIMEMultipart.MIMEMultipart('alternative')
  emailMsg = MIMEMultipart()
  emailMsg['Subject'] = subject
  emailMsg['From'] = sender 
  emailMsg['To'] = ', '.join(to)
  emailMsg['Cc'] = ", ".join(cc)
  #emailMsg.attach(email.mime.text.MIMEText(html,'html'))
  emailMsg.attach(MIMEText(html,'html'))
  #ctype, encoding = mimetypes.guess_type(filenamestr)
  #if ctype is None or encoding is not None:
    # No guess could be made, or the file is encoded (compressed), so
    # use a generic bag-of-bits type.
    #ctype = 'application/octet-stream'
    #print 'came here'
  #maintype, subtype = ctype.split('/', 1)
  fileMsg = MIMEBase('application', "octet-stream")
  fileMsg.set_payload(open(filenamestr,'rb').read())
  #fp = open(filenamestr)
  #fileMsg = email.mime.text.MIMEText(fp.read(), _subtype=subtype)
  #fp.close()
  Encoders.encode_base64(fileMsg)
  fileMsg.add_header('Content-Disposition','attachment;filename='+filenamestr.lstrip(filedir))
  emailMsg.attach(fileMsg)

  # send email
  server = smtplib.SMTP(smtpserver,smtpport)
  server.ehlo()
  server.starttls()
  server.ehlo
  server.login(sender,senderpwd)
  server.sendmail(sender,to+cc,emailMsg.as_string())
  server.close()

#Determining Start and end Dates for this report
enddate = date.today()
enddatestr = enddate.strftime("%d-%m-%Y")
#oneweek = datetime.timedelta(days=7)
#startdate = enddate - oneweek
startdate = date.today() 
startdatestr = startdate.strftime("%d-%m-%Y")
reportfile = sys.argv[1]
dictcsv = csv.DictReader(open(reportfile,'r'))
fillheaders = ['User']
checkheaders = [] 
filterdict = {}
count=0
try:
  for row in dictcsv:
   checkheaders = row.keys()
   checkheaders.remove('User')
   checkheaders.remove('Sl.No')
   rowsum = 0
   for header in checkheaders:
      rowsum = rowsum + int(row[header])
   if rowsum != 0:
     count = count + 1
     for key in row.keys():
        if row[key] != '0':
          if key not in fillheaders:
            fillheaders.append(key)
     filterdict[count] = row
  if len(filterdict.keys()) > 0:
    emailtext = '<table><tr>'
    trtddict = {}
    fillheaders.remove('Sl.No')
    for header in fillheaders:
      emailtext = emailtext + '<td><strong>' + header + '</strong></td>'
    emailtext = emailtext + '</tr>'
    for i in range(1,len(filterdict.keys())+1):
      emailtext = emailtext + '<tr>'
      for header in fillheaders:
        if header in filterdict[i].keys():
          emailtext = emailtext + '<td>' + filterdict[i][header] + '</td>'
        else:
          emailtext = emailtext + '<td>0</td>'
      emailtext = emailtext + '</tr>'
    emailtext = emailtext + '</table>'
  else:
    emailtext = 'No data entry records to report today.'

  mail('[EMS-E2E] Daily DEO Report generated for the date ' + startdatestr, emailtext,reportfile,'logFiles/')
  #print emailtext
except:
  print "Unexpected error:", sys.exc_info()
  print "Exception in user code:"
  print '-'*60
  traceback.print_exc(file=sys.stdout)
  print '-'*60
finally:
  pass
