#ERRORS

registers = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']

def error_type_Var(line):
    if len(line) != 2:
        return (True, "Wrong syntax used for instructions")

    return (False, None)

def error_type_A(line):
    if len(line) != 4:
        return (True, "Wrong syntax used for instructions")

    elif line[1] == 'FLAGS':
        return (True, "Illegal use of FLAGSS register")

    elif line[1] not in registers or line[2] not in registers or line[3] not in registers:
        return (True, "Typos in instruction name or register name")

    return (False, None)

def error_type_B(line):
    if len(line) != 3:
        return (True, "Wrong syntax used for instructions")

    elif line[1] == 'FLAGS':
        return (True, "Illegal use of FLAGS register")

    elif line[1] not in registers:
        return (True, "Typos in instruction name or register name")

    elif not line[2].startswith("$"):
        return (True, "Wrong syntax used for instructions")

    elif not line[2][1:].isdigit():
        return (True, "Illegal Immediate values")

    elif line[2][1:].isdigit():
        if int(line[2][1:]) > 255 or int(line[2][1:]) < 0:
            return (True, "Illegal Immediate values")

    return (False, None)

def error_type_C(line):
    if len(line) != 3:
        return (True, "Wrong syntax used for instructions")

    elif line[1] == 'FLAGS':
        return (True, "Illegal use of FLAGS register")

    elif line[1] not in registers or line[2] not in registers:
        return (True, "Typos in instruction name or register name")

    return (False, None)

def error_type_D(line, variables, labels):
    if len(line) != 3:
        return (True, "Wrong syntax used for instructions")

    elif line[1] == 'FLAGS':
        return (True, "Illegal use of FLAGS register")

    elif line[1] not in registers or line[2] not in registers:
        if line[2] not in variables:
            return (True, "Use of undefined variables")
        elif line[2] in labels:
            return (True, "Misuse of labels as variables")
        elif line[2] in variables:
            return (False, None)
        return (True, "Typos in instruction name or register name")

    return (False, None)

def error_type_E(line, labels, variables):
    if len(line) != 2:
        return (True, "Wrong syntax used for instructions")

    elif line[1] not in labels:
        return (True, "Use of undefined labels")

    elif line[1] in variables:
        return (True, "Misuse of variables as labels")

    return (False, None)

def error_type_F(line):
    if len(line) != 1:
        return (True, "Wrong syntax used for instructions")

    return (False, None)