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

# def MoveToTrgt(trgt :int):
if __name__ == "__main__":
    conn = Connection()
    conn.connect()
    getobj = PLC_GetCommand()
    setobj = PLC_SetTrgtCommand()
    moveobj = PLC_Move()
    '''Set Target Count'''
    settrgt_str1 = setobj.build(1, 22866)
    settrgt_str2 = setobj.build2(1)
    conn.query(settrgt_str1)
    conn.query(settrgt_str2)
    gettrgt_str = getobj.build(1, "TrgtPosi")
    trgt = conn.query(gettrgt_str)
    print(f"Response GetTrgtPosi : {trgt}")
    deci_trgt = ToDecimal(trgt)
    print(f"Trgt Position : {deci_trgt}")
    getposi_str = getobj.build(1, "Posi")
    posi = conn.query(getposi_str)
    print(f"Rsponse GetPopsi : {posi}")
    deci_posi = ToDecimal(posi)
    print(f"Current Position : {deci_posi}") #Checked that it works. 2025.11.14.15:37
    
    '''judge direction and move'''
    if(deci_posi > deci_trgt):
        move_str = moveobj.build(1, "CW", "ON")
        conn.query(move_str)
    elif(deci_posi < deci_trgt):
        move_str = moveobj.build(1, "CCW", "ON")
        conn.query(move_str)
    elif(deci_posi == deci_trgt):
        print(f"No need to move the motor.")
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