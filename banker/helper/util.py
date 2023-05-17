import re
import uuid


def validate_string(str_input):
    return re.match("(^[_\\-\\.0-9a-z]{1,127}$)", str_input) != None or len(str_input)>127 or len(str_input)<1

def validate_balance(num_input):
    return re.match("^(0|([1-9][0-9]*))((\.[0-9]{1,2}|))$", num_input) != None and (0 <= float(num_input)<=4294967295.99)

def create_random_userid():
    return str(uuid.uuid4())
