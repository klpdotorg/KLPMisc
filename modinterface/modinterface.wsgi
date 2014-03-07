import web
import psycopg2
import decimal
import jsonpickle
import csv
import re
from web import form
from ConfigParser import SafeConfigParser

# Needed to find the templates
import sys, os,traceback
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import Utility.KLPDB

urls = (
     '/','modinterface',
     '/submitSYS/(.*)','submitSYS',
)

config = SafeConfigParser()
config.read(os.path.join(os.getcwd(),'config/klpconfig.ini'))
connection = Utility.KLPDB.getConnection()
cursor = connection.cursor()
origimagedir="/images/sysimages/sys/"
outputimagedir="/images/sysimages/school_pics_hash/"


chooseType=form.Form()
chooseType.inputs=(chooseType.inputs+(web.form.Radio('systype',['Comments','Images'],description="Verify : "),))
chooseType.inputs=(chooseType.inputs+(web.form.Button("submit", type="submit", description="Submit"),))

render_plain = web.template.render('templates/')

application = web.application(urls,globals()).wsgifunc()
statements={"get_sys_comments":"select schoolid,id,name,to_char(entered_timestamp,'DD-MM-YYYY'),comments from tb_sys_data where verified='N' and not (comments is null or comments='')",
            "get_sys_images":"select sys.schoolid,sys.id,sys.name,to_char(sys.entered_timestamp,'DD-MM-YYYY'),img.hash_file from tb_sys_images img,tb_sys_data sys where img.sysid=sys.id and img.verified='N'",
            "verify_sys_comments":"update tb_sys_data set verified=%s where id=%s",
            "verify_update_sys_comments":"update tb_sys_data set verified=%s,comments=%s where id=%s",
            "verify_sys_images":"update tb_sys_images set verified=%s where sysid=%s and hash_file=%s",
}


class modinterface:
  def GET(self):
    return render_plain.choosetype(chooseType)
 
  def POST(self):
    input=chooseType()
    self.data=[]
    if not input.validates():
      print "invalid"
      return
    type=""
    if input['systype'].value=='Comments':
       self.data=self.verifyComments()
       type="comments"
    else:
       print 'in images'
       self.data=self.verifyImages()
       type="images"
    web.header('Content-Type','text/html; charset=utf-8')
    return render_plain.modinterface(self.data,type)

  def verifyComments(self):
    sysdata=[]
    try:
      cursor.execute(statements['get_sys_comments'])
      result = cursor.fetchall()
      for row in result:
        sysdata.append({'sid':row[0],'sysid':row[1],'name':row[2],'date':row[3],'comments':row[4]})
      connection.commit()
    except:
      traceback.print_exc(file=sys.stderr)
      connection.rollback()
    return sysdata

  def verifyImages(self):
    sysdata=[]
    try:
      cursor.execute(statements['get_sys_images'])
      result = cursor.fetchall()
      for row in result:
        print row[4]
        sysdata.append({'sid':row[0],'sysid':row[1],'name':row[2],'date':row[3],'images':origimagedir+row[4],'filename':str(row[1])+"|"+row[4]})
      connection.commit()
    except:
      traceback.print_exc(file=sys.stderr)
      connection.rollback()
    print sysdata
    return sysdata


class submitSYS:
  def POST(self,type):
    if type=='comments':
       self.submitComments()
    else:
       self.submitImages()
    web.header('Content-Type','text/html; charset=utf-8')
    return render_plain.sys_verified()


  def submitComments(self):
    print "In Comments"
    i=web.input()
    print i
    verifysysids={}
    for data in i:
      status='R'
      comments=0
      if 'comments' in data:
        sysid=data.split('-')[0]
        comments=1
      else:
         sysid=data
      if sysid not in verifysysids:
         verifysysids[sysid]={"comments":"","status":""}
      if comments:
          verifysysids[sysid]["comments"]=i[data]
      else:
          if i[data]=='Verify':
            status='Y'
          verifysysids[sysid]["status"]=status
    print verifysysids
          
    for sysid in verifysysids:
      try:
          print str(sysid)+" : "+verifysysids[sysid]["status"]
          if verifysysids[sysid]["comments"] == "":
            cursor.execute(statements['verify_sys_comments'],(verifysysids[sysid]["status"],sysid,))
          else:
            cursor.execute(statements['verify_update_sys_comments'],(verifysysids[sysid]["status"],verifysysids[sysid]["comments"],sysid,))
          connection.commit()
      except:
           traceback.print_exc(file=sys.stderr)
           connection.rollback()
          
  def submitImages(self):
    i=web.input()
    print i
    for data in i:
      print data
      print i[data]
      value=i[data]
      status='R'
      sysid=data.split('|')[0]
      filename=data.split('|')[1]
      origfilename=abspath+origimagedir+filename
      if value=='Verify':
        status='Y'
        outputfilename=abspath+outputimagedir+filename
        os.system("convert "+origfilename+" -resize 30% "+outputfilename)
      try:
        cursor.execute(statements['verify_sys_images'],(status,sysid,filename,))
        connection.commit()
      except:
        connection.rollback()
