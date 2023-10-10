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

RAD = core.BROADCAST_ADDR

username_disable = [
    "system",
    "sys",
    "admin",
    "root"
    "superuser"
                    ]

try:
    while True:
        temp = input("\033[34m[+] Please enter your username: ")
        if len(temp.split("@")) >= 2:
            nid_str = temp.split("@")[0]
            un_str = temp.split("@")[1]
            if not nid_str.isdigit() or un_str.lower() in username_disable or int(nid_str) < 0:
                print("\033[31m[$] Please re-enter the username! \033[0m")
                continue
            nid = int(nid_str)
            username = un_str
            break
        if temp.lower() in username_disable:
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
        global RAD
        while True:
            data, address =  rsk.recvfrom(65500)
            msgs = core.jsonBytesToDist(data)
            if msgs == {}: continue
            if "un" not in msgs.keys() or "msg" not in msgs.keys() or "time" not in msgs.keys(): continue
            un = msgs["un"]
            msg = msgs["msg"]
            tn = msgs["time"]
            if un.lower() == "system":
                if msg == "#FC":
                    rsk.sendto(
                        core.distToJsonBytes(
                            core.makeMessage("system", f"#RET:{username}")
                        ),
                        (address[0], core.RECV_PORT)
                    )
                    continue
                elif msg == "#RET":
                    print(f"\033[35m[{address[0]}]\033[34m({tn}) \033[0m> {msg}")
                    continue
                else:
                    pass
            print(f"\033[35m[{address[0]}]\033[34m({tn}) \033[32m{un} \033[0m> {msg}")
    def ASKThread():
        global RAD
        while True:
            data, address = ask.recvfrom(65500)
            msgs = core.jsonBytesToDist(data)
            if msgs == {}: continue
            if "opt" not in msgs.keys() or "arg" not in msgs.keys(): continue
            opt = msgs["opt"]
            arg = msgs["arg"]
            if opt.lower() == "ipbl-add":
                IPBlackList.append(arg)
                print(f"\033[37m[#] Admin => IP BlackList Add: {arg} \033[0m")
            if opt.lower() == "ipbl-del":
                if arg in IPBlackList:
                    IPBlackList.remove(arg)
                print(f"\033[37m[#] Admin => IP BlackList Remove: {arg} \033[0m")
            if opt.lower() == "ipbl-list":
                rsk.sendto(
                    core.distToJsonBytes(
                        core.makeMessage("system", f"#RET:{IPBlackList}")
                    ),
                    (address[0], core.RECV_PORT)
                )
                print(f"\033[37m[#] Admin => IP BlackList List \033[0m")
            if opt.lower() == "eval":
                tmptd = threading.Thread(
                    target=core.runEval,
                    args=(rsk, address, arg)
                )
                tmptd.start()
    def SSKThread():
        global RAD
        while True:
            tmpdata = input("\033[30mInput>\033[37m ")
            if tmpdata == "": continue
            if tmpdata == "#FC":
                ssk.sendto(
                    core.distToJsonBytes(
                        core.makeMessage("system", "#FC")
                    ),
                    core.BROADCAST_ADDR
                )
                continue
            if tmpdata == "#PR":
                RAD = core.BROADCAST_ADDR
                print(f"\033[31m[%] Reset chat address: {RAD} \033[0m")
                continue
            if tmpdata.startswith("$:"):
                if os.path.exists("admin.sign"):
                    spt = tmpdata.split(":")
                    if len(spt) >= 3:
                        opt = spt[1]
                        arg = spt[2]
                        ssk.sendto(
                            core.distToJsonBytes(
                                core.makeAdminMessage(opt, arg)
                            ),
                            RAD
                        )
                        print("\033[33m[#] Send admin message successful! \033[0m")
                        continue
                    else:
                        pass
                else:
                    pass
            if tmpdata.startswith("#P:"):
                spt = tmpdata.split(":")
                if len(spt) >= 2:
                    addr = spt[1]
                    try:
                        rsk.sendto(
                            core.distToJsonBytes(
                                core.makeMessage("system", f"#SWCO:{addr}")
                            ),
                            (addr, core.RECV_PORT)
                        )
                        RAD = (addr, core.RECV_PORT)
                        print(f"\033[31m[%] Successful to set chat address: {RAD} \033[0m")
                        continue
                    except Exception as ex:
                        RAD = core.BROADCAST_ADDR
                        print("\033[31m[!] Error: ",ex,"\033[0m")
                        print(f"\033[31m[!] Reset chat address: {RAD} \033[0m")
                        continue
                else:
                    pass
            ssk.sendto(
                core.distToJsonBytes(
                    core.makeMessage(username, tmpdata)
                ),
                RAD
            )
    # Python Tkinter
    def SSKThreadTK(tmpdata):
        global RAD
        #while True:
        if True:
            #tmpdata = input("\033[30mInput>\033[37m ")
            if tmpdata == "": return
            if tmpdata == "#FC":
                ssk.sendto(
                    core.distToJsonBytes(
                        core.makeMessage("system", "#FC")
                    ),
                    core.BROADCAST_ADDR
                )
                #continue
                return
            if tmpdata == "#PR":
                RAD = core.BROADCAST_ADDR
                print(f"\033[31m[%] Reset chat address: {RAD} \033[0m")
                # continue
                return
            if tmpdata.startswith("$:"):
                if os.path.exists("admin.sign"):
                    spt = tmpdata.split(":")
                    if len(spt) >= 3:
                        opt = spt[1]
                        arg = spt[2]
                        ssk.sendto(
                            core.distToJsonBytes(
                                core.makeAdminMessage(opt, arg)
                            ),
                            RAD
                        )
                        print("\033[33m[#] Send admin message successful! \033[0m")
                        #continue
                        return
                    else:
                        pass
                else:
                    pass
            if tmpdata.startswith("#P:"):
                spt = tmpdata.split(":")
                if len(spt) >= 2:
                    addr = spt[1]
                    try:
                        rsk.sendto(
                            core.distToJsonBytes(
                                core.makeMessage("system", f"#SWCO:{addr}")
                            ),
                            (addr, core.RECV_PORT)
                        )
                        RAD = (addr, core.RECV_PORT)
                        print(f"\033[31m[%] Successful to set chat address: {RAD} \033[0m")
                        #continue
                        return
                    except Exception as ex:
                        RAD = core.BROADCAST_ADDR
                        print("\033[31m[!] Error: ",ex,"\033[0m")
                        print(f"\033[31m[!] Reset chat address: {RAD} \033[0m")
                        # continue
                        return
            else:
                    pass
            ssk.sendto(
                core.distToJsonBytes(
                    core.makeMessage(username, tmpdata)
                ),
                RAD
            )
    RSKT = threading.Thread(target=RSKThread)
    ASKT = threading.Thread(target=ASKThread)
    #SSKT = threading.Thread(target=SSKThread)
    RSKT.start()
    ASKT.start()
    #SSKT.start()
    #RSKT.join()
    #ASKT.join()
    #SSKT.join()

    import tkinter as tk
    root = tk.Tk()
    root.title("Message Sender")
    root.geometry("300x200")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    text = tk.Text(root)
    text.place(x=10, y=10, width=280, height=150)
    text.config(maxundo=0, wrap=tk.WORD, undo=False)
    text.bind("<Key>", lambda e: "break" if len(text.get("1.0", "end-1c")) > 4095 else None)
    button = tk.Button(root, text="Send")
    button.place(x=120, y=170, width=60, height=20)
    button.config(command=lambda: SSKThreadTK(text.get("1.0", "end-1c")))
    root.mainloop()

except Exception as ex:
    print("\033[31m[!] Error: ",ex,"\033[0m")
    exit()