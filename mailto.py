#!/usr/bin/python
# -- encoding:utf8 --
import time
from mailutil import XMail
import subprocess
import os
import sys
import tempfile
import thread
tmp  = tempfile.mktemp()
cfg = """{ 
# 发邮件配置
  "from"   : "d@test.com" ,
  "to"     : ["d@test.com"] ,
  "subject" : "subject",
  "content" : "content",
  "attachs" : [],
  "server" : "mail.test.com",
  "user" : "d@test.com",
  "pass" : os.environ.get("MAILPASS"), # 从环境变量读取密码
  "debug" : False,
  "nologin" : False, #如果在邮件服务器的信任ip列表内，可以不用密码发送邮件
}
"""
with open(tmp,"w") as f:
    f.write(cfg)

def delete_tmp():
    time.sleep(0.1)
    os.remove(tmp)
thread.start_new(delete_tmp,()) 

p = subprocess.call("vi %s" % tmp , shell=True )
if os.path.exists(tmp) :
    with open(tmp,"r") as f:
        msg = f.read()
else :
    quit()

config = eval(msg)
mail = XMail()
mail.config(**config)
mail.send();
print "send done" 


