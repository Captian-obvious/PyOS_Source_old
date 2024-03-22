import PyOS.Filesystem as fs;
import PyOS.UI as ui;
import json,math,os,time;
import threading as task;
import subprocess as runner;
import PyOS.LinuxUtils.psutils as psutils;
import sys;
import ctypes as c;
from ctypes import LibraryLoader;
import base64;
#create the library loader
sys.modules['psutil']=psutils;
lib=c.cdll;
#Load Linux Library
#lin=lib.LoadLibrary('./liblinux.so.2');
#Linux Kernel Utils.
def get_pwd():
    return os.getcwd();
##end
def pwencode(s):
    obfesbytes=[];
    for i in range(len(s)):
        hashed=s[i]+i;
        rshifted=hashed>>4;
        obfesbytes.append(rshifted)
    ##end
    return base64.b64encode(bytes(obfesbytes));
##end
def usrnencode(s):
    obfesbytes=bytearray();
    key=4
    for i in range(len(s)):
        hashed=s[i]+(i+key);
        obfesbytes.append(hashed);
    ##end
    return base64.b64encode(obfesbytes);
##end
def usrndecode(b64):
    obfesbytes=base64.b64decode(b64.encode('ascii'));
    origbytes=bytearray();
    key=4;
    for i in range(len(obfesbytes)):
        orig=obfesbytes[i]-(i+key);
        origbytes.append(orig);
    ##end
    return bytes(origbytes);
##end
def sys_run(cmd):
    return runner.run(cmd,shell=True,capture_output=True);
##end
def sys_read(path):
    exists=os.access(path,os.R_OK);
    if (exists==True):
        f=open(path,'rb');
        bytes=f.read();
        f.close();
        return bytes;
    ##endif
##end
def sys_write(path,data:bytearray|bytes):
    exists=os.access(path,os.W_OK);
    if (exists==True):
        f=open(path,'wb');
        f.write(data);
        f.close();
        return True;
    else:
        return False;
    ##endif
##end
def get_root_dir():
    return os.path.split(os.path.realpath(__file__))[0];
##end
def jsonEncode(data):
    return json.dumps(data);
##end
def jsonDecode(data):
    return json.loads(data);
##end
def run_command(cmd):
    return runner.run(cmd,shell=True);
##end
def execute_prog(path,args):
    runner.call([path]);
##end
def root_exec_path():
    return "/PyOS/.lib";
##end