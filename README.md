# mailto
mailing tool under linux . vi is required.

# config
`vi mailto.py`  
 ```
 修改cfg，以163为例  
 # 发邮件配置  
  "from"   : "d@163.com" ,  
  "to"     : ["d@163.com"] ,  
  "subject" : "subject",
  "content" : "content",
  "attachs" : [],
  "server" : "smtp.163.com",
  "user" : "d@163.com",
  "pass" : os.environ.get("MAILPASS"), # 从环境变量读取密码，自己export MAILPASS=xxxx
  "debug" : False,
  "nologin" : False, #如果在邮件服务器的信任ip列表内，可以不用密码发送邮
  ```  
# usage  
 `python mailto.py`  
 脚本会打开vi , 然后可以修改主题，内容，附件。  
 :wq 保存退出就发送邮件  
 :q! 不保存退出，则放弃发邮件。  
