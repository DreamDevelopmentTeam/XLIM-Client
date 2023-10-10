# encoding:utf-8
import os
import sys
import time
import json
import random
import hashlib
import threading
from socket import *

RECV_PORT = 59800
SEND_PORT = 59810
ADMIN_PORT = 59820
BROADCAST_ADDR = ("255.255.255.255", RECV_PORT)
RECV_ADDR = ("0.0.0.0", RECV_PORT)
SEND_ADDR = ("0.0.0.0", SEND_PORT)
ADMIN_ADDDR = ("0.0.0.0", ADMIN_PORT)



def getRecvSocket():
    sk = socket(AF_INET, SOCK_DGRAM)
    sk.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    sk.bind(RECV_ADDR)
    return sk

def getSendSocket():
    sk = socket(AF_INET, SOCK_DGRAM)
    sk.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    sk.bind(SEND_ADDR)
    return sk

def getAdminSocket():
    sk = socket(AF_INET, SOCK_DGRAM)
    sk.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    sk.bind(ADMIN_ADDDR)
    return sk


def distToJsonBytes(data: dict) -> bytes:
    # coding: utf-8
    jstr = json.dumps(data, ensure_ascii=False)
    return jstr.encode('utf-8')

def jsonBytesToDist(data: bytes) -> dict:
    # coding: utf-8
    try:
        jstr = data.decode('utf-8')
        return json.loads(jstr)
    except Exception as ex:
        return {}


def makeMessage(nid:int, username:str,  msg:str) -> dict:
    return {
        'nid': nid,
        'un': username,
        'msg': msg,
        #'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        'time': time.strftime("%H:%M:%S", time.localtime())
    }

def makeAdminMessage(nid:int, opt:str, arg):
    return  {
        'nid': nid,
        'opt': opt,
        'arg': arg,
    }

def makeSystemMessage(nid:int, opt:str, arg):
    return {
        'nid': nid,
        'opt': opt,
        'arg': arg,
    }

def sendToAll(sk,data):
    sk.sendto(data,BROADCAST_ADDR)


def runEval(nid, rsk,address,arg):
    try:
        rest = eval(arg)
        rsk.sendto(
            distToJsonBytes(
                makeMessage(nid, "system", f"#RET:{rest}")
            ),
            (address[0], RECV_PORT)
        )
    except Exception as ex:
        rsk.sendto(
            distToJsonBytes(
                makeMessage(nid, "system", f"#RET:ERROR:{ex}")
            ),
            (address[0], RECV_PORT)
        )