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
        temp = input("[+] Please enter your username: ")
        if len(temp.split("@")) >= 2:
            nid_str = temp.split("@")[0]
            un_str = temp.split("@")[1]
            if not nid_str.isdigit() or un_str.lower() in username_disable or int(nid_str) < 0:
                print("[$] Please re-enter the username! ")
                continue
            nid = int(nid_str)
            username = un_str
            break
        if temp.lower() in username_disable:
            print("[$] Please re-enter the username! ")
            continue
        username = temp
        break
except Exception as ex:
    print("[!] Error: ",ex,"")
    #print("[$] Please re-enter the username! ")
    exit()

print(f"[$] Hello! {nid} @ {username}! ")

try:
    rsk = core.getRecvSocket()
    ask = core.getAdminSocket()
    ssk = core.getSendSocket()
    print("[+] Protocol is running...")
    def RSKThread():
        global RAD
        while True:
            data, address =  rsk.recvfrom(65500)
            msgs = core.jsonBytesToDist(data)
            if msgs == {}: continue
            if address[0] in IPBlackList: continue
            if "nid" not in msgs.keys() or "un" not in msgs.keys() or "msg" not in msgs.keys() or "time" not in msgs.keys(): continue
            nids = msgs["nid"]
            if nids != nid: continue
            un = msgs["un"]
            msg = msgs["msg"]
            tn = msgs["time"]
            if un.lower() == "system":
                if msg == "#FC":
                    rsk.sendto(
                        core.distToJsonBytes(
                            core.makeMessage(nid, "system", f"#RET:{username}")
                        ),
                        (address[0], core.RECV_PORT)
                    )
                    continue
                elif msg == "#RET":
                    print(f"[{address[0]}]({tn}) > {msg}")
                    continue
                elif msg.startswith("#RET:"):
                    print(f"[{address[0]}]({tn}) > {msg}")
                    continue
                else:
                    pass
            print(f"[{address[0]}]({tn}) {nid} @ {un} > {msg}")
    def ASKThread():
        global RAD
        while True:
            data, address = ask.recvfrom(65500)
            msgs = core.jsonBytesToDist(data)
            if msgs == {}: continue
            if address[0] in IPBlackList: continue
            if "nid" not in msgs.keys() or "opt" not in msgs.keys() or "arg" not in msgs.keys(): continue
            nids = msgs["nid"]
            if nids != nid: continue
            opt = msgs["opt"]
            arg = msgs["arg"]
            if opt.lower() == "ipbl-add":
                IPBlackList.append(arg)
                print(f"[#] Admin => IP BlackList Add: {arg} ")
            if opt.lower() == "ipbl-del":
                if arg in IPBlackList:
                    IPBlackList.remove(arg)
                print(f"[#] Admin => IP BlackList Remove: {arg} ")
            if opt.lower() == "ipbl-list":
                rsk.sendto(
                    core.distToJsonBytes(
                        core.makeMessage(nid, "system", f"#RET:{IPBlackList}")
                    ),
                    (address[0], core.RECV_PORT)
                )
                print(f"[#] Admin => IP BlackList List ")
            if opt.lower() == "eval":
                tmptd = threading.Thread(
                    target=core.runEval,
                    args=(nid, rsk, address, arg)
                )
                tmptd.start()
    def SSKThread():
        global RAD
        while True:
            tmpdata = input("Input> ")
            if tmpdata == "": continue
            if tmpdata == "#FC":
                ssk.sendto(
                    core.distToJsonBytes(
                        core.makeMessage(nid, "system", "#FC")
                    ),
                    core.BROADCAST_ADDR
                )
                continue
            if tmpdata == "#PR":
                RAD = core.BROADCAST_ADDR
                print(f"[%] Reset chat address: {RAD} ")
                continue
            if tmpdata.startswith("$:"):
                if os.path.exists("admin.sign"):
                    spt = tmpdata.split(":")
                    if len(spt) >= 3:
                        opt = spt[1]
                        arg = spt[2]
                        ssk.sendto(
                            core.distToJsonBytes(
                                core.makeAdminMessage(nid, opt, arg)
                            ),
                            RAD
                        )
                        print("[#] Send admin message successful! ")
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
                                core.makeMessage(nid, "system", f"#SWCO:{addr}")
                            ),
                            (addr, core.RECV_PORT)
                        )
                        RAD = (addr, core.RECV_PORT)
                        print(f"[%] Successful to set chat address: {RAD} ")
                        continue
                    except Exception as ex:
                        RAD = core.BROADCAST_ADDR
                        print("[!] Error: ",ex,"")
                        print(f"[!] Reset chat address: {RAD} ")
                        continue
                else:
                    pass
            ssk.sendto(
                core.distToJsonBytes(
                    core.makeMessage(nid, username, tmpdata)
                ),
                RAD
            )
    # Python Tkinter
    def SSKThreadTK(tmpdata):
        global RAD
        #while True:
        if True:
            #tmpdata = input("Input> ")
            if tmpdata == "": return
            if tmpdata == "#FC":
                ssk.sendto(
                    core.distToJsonBytes(
                        core.makeMessage(nid, "system", "#FC")
                    ),
                    core.BROADCAST_ADDR
                )
                #continue
                return
            if tmpdata == "#PR":
                RAD = core.BROADCAST_ADDR
                print(f"[%] Reset chat address: {RAD} ")
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
                                core.makeAdminMessage(nid, opt, arg)
                            ),
                            (RAD[0], core.ADMIN_PORT)
                        )
                        print("[#] Send admin message successful! ")
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
                                core.makeMessage(nid, "system", f"#SWCO:{addr}")
                            ),
                            (addr, core.RECV_PORT)
                        )
                        RAD = (addr, core.RECV_PORT)
                        print(f"[%] Successful to set chat address: {RAD} ")
                        #continue
                        return
                    except Exception as ex:
                        RAD = core.BROADCAST_ADDR
                        print("[!] Error: ",ex,"")
                        print(f"[!] Reset chat address: {RAD} ")
                        # continue
                        return
            else:
                    pass
            ssk.sendto(
                core.distToJsonBytes(
                    core.makeMessage(nid, username, tmpdata)
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
    print("[!] Error: ",ex,"")
    exit()