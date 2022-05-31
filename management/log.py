# Credit : Derfire


#Imports
from datetime import datetime

#Value classes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Type:
    Info=0
    Success=1
    Warn=2
    Error=3

class Output_Type:
    Console=0
    File=1

#Log function

def log(val,type : Type = Type.Info,output_type : Output_Type = Output_Type.Console):
    """Returns the value that has been pass in the parameter and log it in the console or a file.

    Args:
        val (any): the value that you want to log. 
        type (Type, optional): the type of log that you want to log (info,sucess,warn,error). Defaults to Type.Info.
        output_type (Output_Type, optional): [description]. Defaults to Output_Type.Console.

    Returns:
        val (any): the value that has been pass in the parameter (this fonction is a passthrough).
    """
    #get the time of the log

    _now = datetime.now()
    _date = _now.strftime("%d/%m/%Y")
    _hour = _now.strftime("%H:%M:%S")

    #formating the final string relative to the type of the log

    _color = None
    _type = None

    if type == Type.Info:
        _color = Colors.OKCYAN
        _type = "INFO"
    elif type == Type.Success:
        _color = Colors.OKGREEN
        _type = "OK"
    elif type == Type.Warn:
        _color = Colors.WARNING
        _type = "WARN"
    else:
        _color = Colors.FAIL
        _type = "ERROR"
    
        
    _str = Colors.HEADER + f"[{_hour}]" + Colors.ENDC + f"{_color}[{_type}] {str(val)}" + Colors.ENDC

    #return the string

    if output_type == 0:
        return print(_str)
    else:
        return None

