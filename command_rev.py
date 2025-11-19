import socket
from connection import *

conn = Connection()
conn.connect()


def TrgtCount_Converter(value: int):
    hex = f"{value & 0xFFFFFFFF:08X}"
    fixed_hex = hex[4:] + hex[:4]
    print(f"hex : {hex}")
    print(f"fixed hex : {fixed_hex}")
    return fixed_hex #return as string

def ToDecimal(response):#input the raw response, NOT decoded one
        list = []#list to store the strings striped by 4 letters
        response_decode = response.decode() #decoding from byte-style to string
        response_strip = response.rstrip()#eliminating "\r\n"
        '''Stripe by 4 letters'''
        for i in range(0, len(response_strip), 4):
            list.append(response_strip[i:i+4])
            print(f"{i} striped : {response_strip[i:i+4]}")
        #you have to switch the 4 letter 
        outvalue_hex = list[2] + list[1]
        value = int(outvalue_hex, 16)
        return value

class PLC_Commands:
    def __init__(self):
        # Constants for Get command
        self.GET_HEADER = "01SWR002"
        self.GET_TAIL = ",02"
        self.GET_AXIS_FIRST_TERM= {"Posi" : 3, "TrgtPosi" : 2}
        self.GET_AXIS_TAIL = {"Posi" : "21", "TrgtPosi" : "35"}
        # Constants for SetTrgt Command
        self.SET_HEADER = "01WWRD0"  #for cmd str1
        self.SET_TAIL =  ",02,"  #for cmd str1
        self.AXIS_TAIL = "35" #for cmd str1
        self.MEMORYHEADER = "01BWRI021" #for cmd str1
        self.MEMORYTAIL = "1,001,1"
        # Constants for Move Command
        self.Move_HEADER = "01BWRI023"
        self.Move_TAIL = "1,001,"
        self.ONOFF = {"ON" : "1", "OFF" : "0"}
        # Constants for RstCntFlg
        self.RstCntFlg_HEADER = "01BWRI026"
        self.RstCntFlg_TAIL = "1,001,1"
        # Constants for Stop
        self.Stop_COMMAND = "01BWRI02401,001,1"
        
    # ------------Command for GetPosi ot GetTrgtPosi
    def Get(self, axis: int, command_type: str):
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        try:
            axis_tail = self.GET_AXIS_TAIL[command_type]
        except KeyError:
            raise ValueError("Invalid command type (use 'Posi' or 'TrgtPosi')")
        axis_first_term = self.GET_AXIS_FIRST_TERM[command_type] #the number corresponding to axis 1 to 4
        axis_tmp = axis_first_term + 3 * (axis - 1)
        axis_str = f"{axis_tmp:02d}"

        command = self.GET_HEADER + "," + axis_str + axis_tail + self.GET_TAIL + "\r\n"
        conn.query(command)
        print(f"Successfully send Get{command_type} command for axis {axis} : {command}")
        return command
    
    # ------------Command for SetTrgtPosi
    def SetTrgt(self, axis: int, trgt: int):
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        if not (isinstance(trgt, int)):
            raise ValueError("trgt must be an integer")
        axis_tmp = self.GET_AXIS_FIRST_TERM + 3 * (axis - 1) #the first term number of axis part : an arithmetic sequence with a common difference of +3
        axis_str = f"{axis_tmp:02d}"
        
        trgt = TrgtCount_Converter(trgt)
        command = self.SET_HEADER + axis_str + self.AXIS_TAIL +self.SET_TAIL + trgt + "\r\n"
        # print(f"{repr(command)}")
        conn.query(command)
        print(f"Successfully send SetTrgt command1 for axis{axis} to set target to {trgt} : {command}")
        return command
    def SetTrgt2(self, axis: int):
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        axis_tmp = axis - 1 #the first term number of axis part : an arithmetic sequence with a common difference of +3
        axis_str = f"{axis_tmp:01d}"
        command = self.MEMORYHEADER + axis_str + self.MEMORYTAIL + "\r\n"
        # print(f"{repr(command)}")
        conn.query(command)
        print(f"Successfully send SetTrgt command2 for axis{axis} : {command}")
        return command

    def Move(self, axis: int, rot: str, onoff: str):
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        if not (isinstance(rot, str)):
            raise ValueError("rot must be 'CW' or 'CCW'.")
        if (rot == "CW"):
            axis_and_rot = 2 * (axis - 1)
        elif (rot == "CCW"):
            axis_and_rot = 2 * (axis - 1) + 1
        else:
            return False
        axis_and_rot_str = f"{axis_and_rot:01d}"
        command = self.HEADER + axis_and_rot_str + self.Move_TAIL + self.ONOFF[onoff] + "\r\n"
        conn.query(command)
        print(f"Successfully send Move command for axis{axis} to set the {rot} rotation to {onoff}  : {command}")
        return command
    
    def RstCntFlg(self, axis: int):
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        axis_tmp = axis - 1
        axis_str = f"{axis_tmp:01d}"
        command = self.RstCntFlg_HEADER + self.axis_str + self.RstCntFlg_TAIL + "\r\n"
        conn.query(command)
        print(f"Successfully send Reset Couter Flag command for axis{axis} : {command}")
        return command
    
    def Stop(self):
        command = self.Stop_COMMAND + "\r\n"
        conn.query(command)
        print(f"Successfully send All Stop command : {command}")
        return command
        
        
        
 