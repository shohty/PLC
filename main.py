from command import *
from connection import *

def Get(axis, command_type):
    """build a command string and send it via TCP connection"""
    if not (isinstance(axis, int) and 1 <= axis <= 4):
        raise ValueError("axis must be an integer in 1 to 4")
    if not (isinstance(command_type, str) and command_type in ["Posi", "TrgtPosi"]):
        raise ValueError("command_type must be 'Posi' or 'TrgtPosi'")
    obj = GetCommand()
    command = obj.build(axis, command_type)
    # tcp_conn(command)
    # return True
    return command

def SetTrgt(axis:int, trgt:int):
    """build a command string and send it via TCP connection"""
    if not (isinstance(axis, int) and 1 <= axis <= 4):
        raise ValueError("axis must be an integer in 1 to 4.")
    if not (isinstance(trgt, int)):
        raise ValueError("trgt must be an integer.")

    obj = SetTrgtCommand()
    command = obj.build(axis, trgt)
    tcp_conn(command)
    return True

def Consistency_Check(axis:int, trgt:int):
    setobj = SetTrgtCommand()
    setcommand = setobj.build(axis, trgt)
    tcp_conn(setcommand)
    getobj = GetCommand()
    gettrgtcommand = getobj.build(axis, "TrgtPosi")
    check = tcp_conn(gettrgtcommand)
    print(f"{check} : Consistent with {trgt}")
    
    
if __name__ == "__main__":
    conn = PLCConnection()
    conn.connect()
    getobj = GetCommand()
    setobj = SetTrgtCommand()
    # command_string = getobj.build(1,"Posi")
    settrgtcommand_string = setobj.build(1, -5000) #cmd str 1
    settrgtcommand_string2 = setobj.build2(1) #cmd str 2
    getcommand_string = getobj.build(1,"TrgtPosi")
    conn.send(settrgtcommand_string2)
    conn.send(settrgtcommand_string)
    gettrgt = conn.send(getcommand_string)
    print(f"Trgt Position : {gettrgt}")
    conn.close()
    # Get(1, "Posi")
    # SetTrgt(1, 500)
    #Get(1, "TrgtPosi")
    # Get(1, "TrgtPosi")
    #Consistency_Check(1, 500)