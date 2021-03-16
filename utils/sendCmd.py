import threading
import socket

from rest_framework.utils import json

'''
{type:'download',option:'active' ,serialnum:'要激活的设备的序列号',key:'设备的秘钥'}
修改阈值
{type:'download',option:'updateconf',serialnum:'要激活的设备的序列号',key:'设备的秘钥'}
'''
class SendCmd(threading.Thread):
    ret = {"type":'download',"option":'active' ,"serialnum":'要激活的设备的序列号',"key":'设备的秘钥',"status":1}
    def __init__(self,option,serialnum):
        threading.Thread.__init__(self)
        self.ret["option"] = option
        self.ret["serialnum"] = serialnum
    def run(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 20001))
            s.sendall(json.dumps(self.ret).encode("utf-8"))
        except Exception as e:
            print(e)
