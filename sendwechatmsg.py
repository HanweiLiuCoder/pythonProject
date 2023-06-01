import wxmpy

name = "code-org"  # 改成自己的  username  和 userpwd
pwd = "Cc20051128"
txt1 = "a"
txt2 = "b"
txt3 = "c"
result = wxmpy.sendMsgToUser(name, pwd, txt1, txt2, txt3)

wxmpy.init(name, pwd)
result = wxmpy.sendMsg(txt1, txt2, txt3)
print(result)