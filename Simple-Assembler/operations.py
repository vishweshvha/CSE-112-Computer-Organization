# ISA OPERATIONS

# OPCODES for reference
# add 00000 | sub 00001 | mov $Imm 00010 | mov 00011 | ld 00100 | st 00101
# mul 00110 | div 00111 | rs 01000 | ls 01001 | xor 01010 | or 01011 | and 01100
# invert 01101 | cmp 01110 | jmp 01111 | jlt 10000 | jgt 10001 | je 10010 | hlt 10011

#-----------------------------------------------------------------------------------

def regFind(register):
    if register == 'R0':
        return '000'
    elif register == 'R1':
        return '001'
    elif register == 'R2':
        return '010'
    elif register == 'R3':
        return '011'
    elif register == 'R4':
        return '100'
    elif register == 'R5':
        return '101'
    elif register == 'R6':
        return '110'
    elif register == 'FLAGS':
        return '111'
    else:
        errors.error_a()

def binary(num):
    num = int(num)
    bnr = bin(num).replace('0b','')
    x = bnr[::-1]
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr

def assembly_code_builder(assembly_code):
    labels = []
    line_number = 0
    for line in assembly_code:
        if line[0] == 'var':
            line_number -= 1
        if line[0][-1] == ':':
            labels.append(line[0][:-1])
            labels.append(binary(line_number))
            line.remove(line[0])
        line_number += 1

    for line in assembly_code:
        if line != []:
            if line[0] == 'jmp':
                if line[1] in labels:
                    line[1] = labels[labels.index(line[1])+1]

            elif line[0] == 'jlt':
                if line[1] in labels:
                    line[1] = labels[labels.index(line[1])+1]

            elif line[0] == 'jgt':
                if line[1] in labels:
                    line[1] = labels[labels.index(line[1])+1]

            elif line[0] == 'je':
                if line[1] in labels:
                    line[1] = labels[labels.index(line[1])+1]

    return assembly_code, labels


# Performs reg1 = reg2 + reg3. If the computation
# overflows, then the overflow flag is set
# A | opcode (unused 2bits) reg1 reg2 reg3
def add(reg1, reg2, reg3, line_number):
    return '00000' + '00' + regFind(reg1) + regFind(reg2) + regFind(reg3)

# Performs reg1 = reg2 - reg3. In case reg3 > reg2,
# 0 is written to reg1 and overflow flag is set.
# A |opcode (unused 2bits) reg1 reg2 reg3
def sub(reg1, reg2, reg3, line_number):
    return '00001' + '00' + regFind(reg1) + regFind(reg2) + regFind(reg3)


# Performs reg1 = $Imm where Imm is a 8 bit value.
# B | opcode(5bits) reg1 immediatevalue(8bits)
def moveImmediate(reg1, value, line_number):
    return '00010' + regFind(reg1) + binary(int(value))


# Performs reg1 = reg2.
# C | opcode unused(5bits) reg1 reg2
def moveRegister(reg1, reg2, line_number):
    return '00011' + '00000' + regFind(reg1) + regFind(reg2)


# Loads data from mem_addr into reg1.
# D | opcode reg1 memory(8bits)
def load(reg1, value,line_number,variables):
    if value in variables:
        index = variables.index(value)
        return '00100' + regFind(reg1) + binary(int(variables[index+1]))

    return '00100' + regFind(reg1) + binary(int(value))


# Stores data from reg1 to mem_addr.
# D | opcode reg1 memory(8bits)
def store(reg1, value,line_number,variables):
    if value in variables:
        index = variables.index(value)
        return '00101' + regFind(reg1) + binary(int(variables[index+1]))

    return '00101' + regFind(reg1) + binary(int(value))


# Performs reg1 = reg2 x reg3. If the computation
# overflows, then the overflow flag is set.
# A |opcode (unused 2bits) reg1 reg2 reg3
def mul(reg1, reg2, reg3, line_number):
    return '00110' + '00' + regFind(reg1) + regFind(reg2) + regFind(reg3)


# Performs reg3/reg4. Stores the quotient
# in R0 and the remainder in R1.
# C | opcode unused(5bits) reg1 reg2
def div(reg1, reg2, line_number):
    return '00111' + '00000' + regFind(reg1) + regFind(reg2)


# Right shifts reg1 by $Imm,
# where $Imm is an 8 bit value.
# B | opcode(5bits) reg1 immediatevalue(8bits)
def rightShift(reg1, value,line_number):
    return '01000' + regFind(reg1) + binary(int(value))


# Left shifts reg1 by $Imm,
# where $Imm is an 8 bit value.
# B | opcode(5bits) reg1 immediatevalue(8bits)
def leftShift(reg1, value,line_number):
    return '01001' + regFind(reg1) + binary(int(value))


# Performs bitwise XOR of reg2 and reg3.
# Stores the result in reg1.
# A |opcode (unused 2bits) reg1 reg2 reg3
def xor(reg1, reg2, reg3, line_number):
    return '01010' + '00' + regFind(reg1) + regFind(reg2) + regFind(reg3)


# Performs bitwise OR of reg2 and reg3.
# Stores the result in reg1.
# A |opcode (unused 2bits) reg1 reg2 reg3
def Or(reg1, reg2, reg3, line_number):
    return '01011' + '00' + regFind(reg1) + regFind(reg2) + regFind(reg3)


# Performs bitwise AND of reg2 and reg3.
# Stores the result in reg1.
# A |opcode (unused 2bits) reg1 reg2 reg3
def And(reg1, reg2, reg3, line_number):
    return '01100' + '00' + regFind(reg1) + regFind(reg2) + regFind(reg3)


# Performs bitwise NOT of reg2.
# Stores the result in reg1.
# C | opcode unused(5bits) reg1 reg2
def invert(reg1, reg2, line_number):
    return '01101' + '00000' + regFind(reg1) + regFind(reg2)


# Compares reg1 and reg2 and sets up the FLAGS register.
# C | opcode unused(5bits) reg1 reg2
def compare(reg1, reg2, line_number):
    return '01110' + '00000' + regFind(reg1) + regFind(reg2)


# Jumps to mem_addr, where mem_addr is a memory address.
# E | opcode unused(3bits) memory(8bits)
def jmp(value, line_number):
    return '01111' + '000' + str(value)


# Jump to mem_addr if the less than flagis set (less than
# flag = 1), where mem_addr is a memory address.
# E | opcode unused(3bits) memory(8bits)
def jlt(value, line_number):
    return '10000' + '000' + str(value)


# Jump to mem_addr if the greater than flag is set (greater than
# flag = 1), where mem_addr is a memory address.
# E | opcode unused(3bits) memory(8bits)
def jgt(value, line_number):
    return '10001' + '000' + str(value)


# Jump to mem_addr if the equal flag is set (equal flag =
# 1), where mem_addr is a memory address.
# E | opcode unused(3bits) memory(8bits)
def je(value, line_number):
    return '10010' + '000' + str(value)


# Stops the machine from executing until reset
# F | opcode unused(11bits)
def hlt():
    return '10011' + '00000000000'