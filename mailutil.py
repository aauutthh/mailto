#!/usr/bin/python
# -- encoding:utf8 -- 
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart   
from email.header import Header
#from smtplib import SMTP_SSL as SMTP
from smtplib import SMTP as SMTP
import os
import tempfile
import time
#from subprocess import Popen ,PIPE

def createmail(sender ,to_list, subject , content) :
    msg = MIMEMultipart('related') ##采用related定义内嵌资源的邮件体  
    msgtext = MIMEText(content,_subtype='plain',_charset='utf-8') ##_subtype有plain,html等格式，避免使用错误  
    msg.attach(msgtext)  
    msg['Subject'] = Header(subject  ,'utf8')
    msg['From'] = sender
    msg['To'] = ";".join(to_list)  
    return msg
def createattach( atfile):  
    attach = MIMEText(open(atfile,'rb').read() ,_charset='utf-8')   
    attach.replace_header("Content-Transfer-Encoding" , 'base64')
    attach["Content-Type"] = 'application/octet-stream'  
    attach["Content-Disposition"] = 'attachment; filename='+os.path.basename(atfile)
    return attach
def createmail_withatt(sender ,to_list, subject , content , att_list) :
    msg = createmail(sender, to_list, subject, content)
    for att in att_list :
        msg.attach(createattach(att))  
    return msg
  
class XMail :
    _subject_ = "XMail"
    _content_ = "XMail auto send"
    _contentfile_ = None
    _from_ = "test@XMail.com"
    _to_ = ["test@XMail.com"]
    _attachs_ = ["/proc/cpuinfo"]
    _server_ = "smtp.163.com"
    _user_ = "xx"
    _pass_ = "xx"
    _debug_ = False
    _nologin_ = False
    def __init__(self , **config) :
        self.config(**config)

    def config(self , **config) :
        if len(config) > 0 : 
            self._from = config.get("from" , self._from_) 
            self._to = config.get("to" , self._to_) 
            if not isinstance(self._to, list) :
                self._to = [str(self._to)] 
            self._subject = config.get("subject" , self._subject_) 
            self._contentfile = config.get("contentfile" , self._contentfile_) 
            if self._contentfile :
                self._content = open(self._contentfile,"r").read()
            else :
                self._content = config.get("content" , self._content_) 
            self._attachs = config.get("attachs" , self._attachs_) 
            self._server = config.get("server" , self._server_) 
            self._user = config.get("user" , self._user_) 
            self._pass = config.get("pass" , self._pass_) 
            self._debug = config.get("debug" , self._debug_) 
            self._nologin = config.get("nologin" , self._nologin_) 

    def send(self):
        msg = createmail_withatt(self._from, self._to, self._subject, self._content , self._attachs)
        smtp = SMTP()
        if self._debug :
            smtp.set_debuglevel(1)
        try :
            smtp.connect(self._server)
            if not self._nologin :
                smtp.login(self._user, self._pass)
        except Exception , e :
            print e
        else :
            smtp.sendmail(self._from, self._to, msg.as_string())
            #smtp.sendmail("daniel", self._to, msg.as_string())
        smtp.quit()
        
    
if __name__ == "__main__":
    config = { 
      "from"   : "d@test.com" ,
      "to"     : ["d@test.com"] ,
      "subject" : "sys alarm",
      "content" : "hello",
      "contentfile" : "/proc/cpuinfo", # 如果指定了内容文件，则会覆盖content
      "attachs" : ["/proc/cpuinfo"],
      "server" : "mail.test.com",
      "user" : "d@test.com",
      "pass" : os.environ.get("MAILPASS"),
      "nologin" : False, # 当邮件服务器信任你发信的ip时，不需要用户名密码登陆
      "debug" : True,
    }

    mail = XMail()
    mail.config(**config)
    mail.send();

