import socket

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
class PLC_GetCommand:
    """This is the class for Get Command.(GetPosi,GetTrgtPosi)"""
    def __init__(self):
    # prequuisite for "Get" command
        self.header = "01SWR002" #the overall header
        self.tail = ",02" #the overall tail
        self.axis_first_term = {"Posi" : 3, "TrgtPosi" : 2} #the first term number of axis part : an arithmetic sequence with a common difference of +3
        self.axis_tail = {"Posi" : "21", "TrgtPosi" : "35"}
    
    def build(self, axis: int, command_type: str):
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        try:
            axis_tail = self.axis_tail[command_type]
        except KeyError:
            raise ValueError("Invalid command type (use 'Posi' or 'TrgtPosi')")
        axis_first_term = self.axis_first_term[command_type] #the number corresponding to axis 1 to 4
        axis_tmp = axis_first_term + 3 * (axis - 1)
        axis_str = f"{axis_tmp:02d}"

        command = self.header + "," + axis_str + axis_tail + self.tail + "\r\n"
        print(f"{command}")
        return command
    
class PLC_SetTrgtCommand:
    def __init__(self):
        self.header = "01WWRD0" #for cmd str1
        self.tail = ",02," #for cmd str1
        self.axis_first_term = 2 #for cmd str1
        self.axis_tail = "35" #for cmd str1
        self.memoryheader = "01BWRI021"
        self.memorytail = "1,001,1"
    
    def build(self, axis: int, trgt: int):#cmd str1 setting the trgt axis position
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        if not (isinstance(trgt, int)):
            raise ValueError("trgt must be an integer")
        axis_tmp = self.axis_first_term + 3 * (axis - 1) #the first term number of axis part : an arithmetic sequence with a common difference of +3
        axis_str = f"{axis_tmp:02d}"
        
        trgt = TrgtCount_Converter(trgt)
        command = self.header + axis_str + self.axis_tail +self.tail + trgt + "\r\n"
        # print(f"{repr(command)}")
        print(f"{command}")
        return command
    
    def build2(self, axis: int):#cmd str2 setting the memory address for each axis
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        axis_tmp = axis - 1 #the first term number of axis part : an arithmetic sequence with a common difference of +3
        axis_str = f"{axis_tmp:01d}"
        command = self.memoryheader + axis_str + self.memorytail + "\r\n"
        print(f"{repr(command)}")
        return command
    
class PLC_Move():
    '''This is the command for rotating the motor and '''
    def __init__(self):
        self.header = "01BWRI023"
        self.tail = "1,001,"
        self.ONOFF = {"ON" : "1", "OFF" : "0"}
    def build(self, axis: int, rot: str, onoff: str):
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
        command = self.header + axis_and_rot_str + self.tail + self.ONOFF[onoff] + "\r\n"
        return command

class PLC_RstCntFlg():
    '''This is the command for killing the flag already turned on'''
    def __init__(self):
        self.header = "01BWRI026"
        self.tail = "1,001,1"
    def build(self, axis: int):
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        axis_tmp = axis - 1
        axis_str = f"{axis_tmp:01d}"
        command = self.header + self.axis_str + self.tail + "\r\n"
        return command

class PLC_Stop():
    '''This is the command for terminating all motors'''
    def __init__(self):
        self.command = "01BWRI02401,001,1"
    def build(self):
        command = self.command + "\r\n"
        return command          
      
def GetCommand_check():
    """"Unit test for GetCommand class."""
    getposi_command = ["01SWR002,0321,02\r\n", "01SWR002,0621,02\r\n", "01SWR002,0921,02\r\n", "01SWR002,1221,02\r\n"]
    gettrgtposi_command = ["01SWR002,0235,02\r\n", "01SWR002,0535,02\r\n", "01SWR002,0835,02\r\n", "01SWR002,1135,02\r\n"]
    obj = PLC_GetCommand()
    for i in range(4):
        getposi = obj.build(i+1, "Posi")
        gettrgtposi = obj.build(i+1, "TrgtPosi")
        assert getposi == getposi_command[i], f"× : Expected '01SWR002,0321,02' but got {getposi}"
        assert gettrgtposi == gettrgtposi_command[i], f"× : Expected '01SWR002,0321,02' but got {getposi}"
        print(f"✓ : axis {i+1} GetPosi and GetTrgtPosi command test passed.")
        
def SetTrgtCommand_check():
    """"Unit test for GetCommand class."""
    settrgt_command = ["01WWRD00235,02,01900000\r\n","01WWRD00535,02,01900000\r\n","01WWRD00835,02,01900000\r\n","01WWRD01135,02,01900000\r\n"] #trgtcount is 400
    obj = PLC_SetTrgtCommand()
    for i in range(4):
        settrgt = obj.build(i+1, 400)
        assert settrgt == settrgt_command[i], f"× : Expected {settrgt_command[i]} but got {settrgt}"
        print(f"✓ : axis {i+1} SetTrgtPosi command test passed.")
