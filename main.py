from command import *
from connection import *


def GetPosi(axis):#Getするための一時的な関数(main関数setobj = ...以降に使用)
    getposi_string = getobj.build(1, "Posi")
    getposi = conn.send(getposi_string)
    print(f"getposi: {getposi}")
    return getposi

def GetTrgtPosi(axis):
    gettrgtposi_string = getobj.build(axis, "TrgtPosi")
    gettrgtposi = conn.send(gettrgtposi_string)
    print(f"getposi: {gettrgtposi}")
    return gettrgtposi

    
if __name__ == "__main__":
    conn = PLC_Connection()
    conn.connect()
    getobj = PLC_GetCommand()
    setobj = PLC_SetTrgtCommand()
    settrgt_str1 = setobj.build(1,801)
    settrgt_str2 = setobj.build2(1)
    conn.send(settrgt_str1)
    conn.send(settrgt_str2)    
    gettrgt_str = getobj.build(1, "TrgtPosi")
    conn.send(gettrgt_str)
    # command_string = getobj.build(1,"Posi")
    # settrgtcommand_string = setobj.build(1, -5000) #cmd str 1
    # settrgtcommand_string2 = setobj.build2(1) #cmd str 2
    # getcommand_string = getobj.build(1,"TrgtPosi")
    # conn.send(settrgtcommand_string2)
    # conn.send(settrgtcommand_string)
    # gettrgt = conn.send(getcommand_string)
    # print(f"Trgt Position : {gettrgt}")
    conn.close()
    # Get(1, "Posi")
    # SetTrgt(1, 500)
    #Get(1, "TrgtPosi")
    # Get(1, "TrgtPosi")
    #Consistency_Check(1, 500)