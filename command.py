import socket

def TrgtCount_Converter(value: int):
    hex8 = f"{value & 0xFFFFFFFF:08X}"
    swapped = hex8[4:] + hex8[:4]
    print(f"hex8 : {hex8}")
    print(f"swapped : {swapped}")
    return swapped #return as string

class GetCommand:
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

class SetTrgtCommand:
    def __init__(self):
        self.header = "01WWRD0" #for cmd str1
        self.tail = ",02," #for cmd str1
        self.axis_first_term = 2 #for cmd str1
        self.axis_tail = "35" #for cmd str1
        self.memoryheader = "01BWRT021"
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
        print(f"{command}")
        return command
    
    def build2(self, axis: int):#cmd str2 setting the memory address for each axis
        if not (isinstance(axis, int) and 1 <= axis <= 4):
            raise ValueError("axis must be an integer in 1 to 4")
        
        axis_tmp = axis - 1 #the first term number of axis part : an arithmetic sequence with a common difference of +3
        axis_str = f"{axis_tmp:02d}"
        command = self.memoryheader + axis_str + self.memorytail + "\r\n"
        print(f"{command}")
        return command
    
def GetCommand_check():
    """"Unit test for GetCommand class."""
    getposi_command = ["01SWR002,0321,02\r\n", "01SWR002,0621,02\r\n", "01SWR002,0921,02\r\n", "01SWR002,1221,02\r\n"]
    gettrgtposi_command = ["01SWR002,0235,02\r\n", "01SWR002,0535,02\r\n", "01SWR002,0835,02\r\n", "01SWR002,1135,02\r\n"]
    obj = GetCommand()
    for i in range(4):
        getposi = obj.build(i+1, "Posi")
        gettrgtposi = obj.build(i+1, "TrgtPosi")
        assert getposi == getposi_command[i], f"× : Expected '01SWR002,0321,02' but got {getposi}"
        assert gettrgtposi == gettrgtposi_command[i], f"× : Expected '01SWR002,0321,02' but got {getposi}"
        print(f"✓ : axis {i+1} GetPosi and GetTrgtPosi command test passed.")
        
def SetTrgtCommand_check():
    """"Unit test for GetCommand class."""
    settrgt_command = ["01WWRD00235,02,01900000\r\n","01WWRD00535,02,01900000\r\n","01WWRD00835,02,01900000\r\n","01WWRD01135,02,01900000\r\n"] #trgtcount is 400
    obj = SetTrgtCommand()
    for i in range(4):
        settrgt = obj.build(i+1, 400)
        assert settrgt == settrgt_command[i], f"× : Expected {settrgt_command[i]} but got {settrgt}"
        print(f"✓ : axis {i+1} SetTrgtPosi command test passed.")
    
        
if __name__ == "__main__":
    GetCommand_check()