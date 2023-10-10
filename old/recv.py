# encoding:utf-8
import os
import sys
import time
import json
import random
import socket
import hashlib
import threading

import core

IPBlackList = []

nid = 0
username = "Null"

try:
    while True:
        temp = input("\033[34m[+] Please enter your username: ")
        if len(temp.split("@")) >= 2:
            nid_str = temp.split("@")[0]
            un_str = temp.split("@")[1]
            if not nid_str.isdigit() or un_str.lower() == "system" or int(nid_str) < 0:
                print("\033[31m[$] Please re-enter the username! \033[0m")
                continue
            nid = int(nid_str)
            username = un_str
            break
        if temp.lower() == "system":
            print("\033[31m[$] Please re-enter the username! \033[0m")
            continue
        username = temp
        break
except Exception as ex:
    print("\033[31m[!] Error: ",ex,"\033[0m")
    #print("\033[31m[$] Please re-enter the username! \033[0m")
    exit()

print(f"\033[33m[$] Hello! {nid} @ {username}! \033[0m")

try:
    rsk = core.getRecvSocket()
    ask = core.getAdminSocket()
    ssk = core.getSendSocket()
    print("\033[32m[+] Protocol is running...\033[0m")
    def RSKThread():
        while True:
            data, address =  rsk.recvfrom(65500)



except Exception as ex:
    print("\033[31m[!] Error: ",ex,"\033[0m")
    exit()