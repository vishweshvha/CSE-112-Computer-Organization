#Done By
#Vishwesh Vhavle, 2020156
#Dev Thakkar, 2020052
#Sahil Deshpande, 2020114

from sys import stdin
import matplotlib.pyplot as plt

PC = 0
R0 = '0000000000000000'
R1 = '0000000000000000'
R2 = '0000000000000000'
R3 = '0000000000000000'
R4 = '0000000000000000'
R5 = '0000000000000000'
R6 = '0000000000000000'
FLAGS = '0000000000000000'

halt = False

#Initialze MEM to 0
MEM = ['0000000000000000'] * 256

#Taking Input
machine_code = []
for line in stdin:
    if line == '':
        break
    else:
        machine_code.append(line.split())

#Removes Empty Lines
for i in range(len(machine_code)-1,-1,-1):
    if machine_code[i] == []:
        machine_code.pop(i)

#Loading Memory
for i in range(len(machine_code)):
    MEM[i] = machine_code[i][0]

def binaryToDecimal(num):
    return int(num, 2)

def decimalToBinary(num):
    num = int(num)
    bnr = bin(num).replace('0b','')
    x = bnr[::-1]
    while len(x) < 16:
        x += '0'
    bnr = x[::-1]
    return bnr

def decimalToBinary8(num):
    num = int(num)
    bnr = bin(num).replace('0b','')
    x = bnr[::-1]
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr

def MEM_value(mem_addr):
    decimal_mem_addr = binaryToDecimal(mem_addr)
    return MEM[decimal_mem_addr]

def RF(register):
    global R0, R1, R2, R3, R4, R5, R6, FLAGS

    if register == '000':
        return R0
    elif register == '001':
        return R1
    elif register == '010':
        return R2
    elif register == '011':
        return R3
    elif register == '100':
        return R4
    elif register == '101':
        return R5
    elif register == '110':
        return R6
    elif register == '111':
        return FLAGS

def RegStore(register, value):
    global R0, R1, R2, R3, R4, R5, R6, FLAGS

    if register == '000':
        R0 = value
    elif register == '001':
        R1 = value
    elif register == '010':
        R2 = value
    elif register == '011':
        R3 = value
    elif register == '100':
        R4 = value
    elif register == '101':
        R5 = value
    elif register == '110':
        R6 = value
    elif register == '111':
        FLAGS = value

# Performs reg1 = reg2 + reg3. If the computation
# overflows, then the overflow flag is set
# A | opcode (unused 2bits) reg1 reg2 reg3
def add(reg1, reg2, reg3):
    value = binaryToDecimal(RF(reg2)) + binaryToDecimal(RF(reg3))
    if value > 255:
        RegStore('111', '0000000000001000')
        RegStore(reg1, decimalToBinary(255))
    else:
        RegStore(reg1, decimalToBinary(value))


# Performs reg1 = reg2 - reg3. In case reg3 > reg2,
# 0 is written to reg1 and overflow flag is set.
# A |opcode (unused 2bits) reg1 reg2 reg3
def sub(reg1, reg2, reg3):
    value = binaryToDecimal(RF(reg2)) - binaryToDecimal(RF(reg3))
    if value < 0:
        RegStore('111', '0000000000001000')
        RegStore(reg1, decimalToBinary(0))
    else:
        RegStore(reg1, decimalToBinary(value))


# Performs reg1 = $Imm where Imm is a 8 bit value.
# B | opcode(5bits) reg1 immediatevalue(8bits)
def moveImmediate(reg1, value):
    value = binaryToDecimal(value)
    RegStore(reg1, decimalToBinary(value))


# Performs reg1 = reg2.
# C | opcode unused(5bits) reg1 reg2
def moveRegister(reg1, reg2):
    RegStore(reg1, RF(reg2))
    RegStore('111','0000000000000000')


# Loads data from mem_addr into reg1.
# D | opcode reg1 memory(8bits)
def load(reg1, value):
    mem_addr = binaryToDecimal(value)
    RegStore(reg1, MEM[mem_addr])


# Stores data from reg1 to mem_addr.
# D | opcode reg1 memory(8bits)
def store(reg1, value):
    mem_addr = binaryToDecimal(value)
    MEM[mem_addr] = RF(reg1)


# Performs reg1 = reg2 x reg3. If the computation
# overflows, then the overflow flag is set.
# A |opcode (unused 2bits) reg1 reg2 reg3
def mul(reg1, reg2, reg3):
    value = binaryToDecimal(RF(reg2)) * binaryToDecimal(RF(reg3))
    if value < 0:
        RegStore('111', '0000000000001000')
        RegStore(reg1, decimalToBinary(0))
    elif value > 255:
        RegStore('111', '0000000000001000')
        RegStore(reg1, decimalToBinary(255))
    else:
        RegStore(reg1, decimalToBinary(value))


# Performs reg3/reg4. Stores the quotient
# in R0 and the remainder in R1.
# C | opcode unused(5bits) reg1 reg2
def div(reg1, reg2):
    quotient = binaryToDecimal(RF(reg1)) / binaryToDecimal(RF(reg2))
    remainder = binaryToDecimal(RF(reg1)) / binaryToDecimal(RF(reg2))
    RegStore('000', decimalToBinary(quotient))
    RegStore('001', decimalToBinary(remainder))


# Right shifts reg1 by $Imm,
# where $Imm is an 8 bit value.
# B | opcode(5bits) reg1 immediatevalue(8bits)
def rightShift(reg1, value):
    num = binaryToDecimal(value)
    instruction = RF(reg1)
    instruction = ('0' * num) + instruction[:len(instruction)-num]
    RegStore(reg1, instruction)


# Left shifts reg1 by $Imm,
# where $Imm is an 8 bit value.
# B | opcode(5bits) reg1 immediatevalue(8bits)
def leftShift(reg1, value):
    num = binaryToDecimal(value)
    instruction = RF(reg1)
    instruction += ('0' * num)
    instruction = instruction[len(instruction)-16:]
    RegStore(reg1, instruction)


# Performs bitwise XOR of reg2 and reg3.
# Stores the result in reg1.
# A |opcode (unused 2bits) reg1 reg2 reg3
def xor(reg1, reg2, reg3):
    value1 = binaryToDecimal(RF(reg2))
    value2 = binaryToDecimal(RF(reg3))
    RegStore(reg1, decimalToBinary(value1 ^ value2))


# Performs bitwise OR of reg2 and reg3.
# Stores the result in reg1.
# A |opcode (unused 2bits) reg1 reg2 reg3
def Or(reg1, reg2, reg3):
    value1 = binaryToDecimal(RF(reg2))
    value2 = binaryToDecimal(RF(reg3))
    RegStore(reg1, decimalToBinary(value1 | value2))


# Performs bitwise AND of reg2 and reg3.
# Stores the result in reg1.
# A |opcode (unused 2bits) reg1 reg2 reg3
def And(reg1, reg2, reg3):
    value1 = binaryToDecimal(RF(reg2))
    value2 = binaryToDecimal(RF(reg3))
    RegStore(reg1, decimalToBinary(value1 & value2))


# Performs bitwise NOT of reg2.
# Stores the result in reg1.
# C | opcode unused(5bits) reg1 reg2
def invert(reg1, reg2):
    value1 = RF(reg2)
    value2 = value1.replace('0', 't')
    value2 = value2.replace('1', '0')
    value2 = value2.replace('t', '1')
    RegStore(reg1, value2)


# Compares reg1 and reg2 and sets up the FLAGS register.
# C | opcode unused(5bits) reg1 reg2
def compare(reg1, reg2):
    value1 = binaryToDecimal(RF(reg1))
    value2 = binaryToDecimal(RF(reg2))
    if value1 < value2:
        RegStore('111', '0000000000000100')
    elif value1 > value2:
        RegStore('111', '0000000000000010')
    elif value1 == value2:
        RegStore('111', '0000000000000001')


# Jumps to mem_addr, where mem_addr is a memory address.
# E | opcode unused(3bits) memory(8bits)
def jmp(value):
    global PC, FLAGS
    PC = binaryToDecimal(value)
    FLAGS = '0000000000000000'


# Jump to mem_addr if the less than flagis set (less than
# flag = 1), where mem_addr is a memory address.
# E | opcode unused(3bits) memory(8bits)
def jlt(value):
    global FLAGS
    if FLAGS == '0000000000000100':
        global PC
        PC = binaryToDecimal(value)
    FLAGS = '0000000000000000'


# Jump to mem_addr if the greater than flag is set (greater than
# flag = 1), where mem_addr is a memory address.
# E | opcode unused(3bits) memory(8bits)
def jgt(value):
    global FLAGS
    if FLAGS == '0000000000000010':
        global PC
        PC = binaryToDecimal(value)
    FLAGS = '0000000000000000'


# Jump to mem_addr if the equal flag is set (equal flag =
# 1), where mem_addr is a memory address.
# E | opcode unused(3bits) memory(8bits)
def je(value):
    global FLAGS
    if FLAGS == '0000000000000001':
        global PC
        PC = binaryToDecimal(value)
    FLAGS = '0000000000000000'


def execute(instruction, PC):
    if instruction[:5] == '00000':
        add(instruction[7:10],instruction[10:13],instruction[13:])

    elif instruction[:5] == '00001':
        sub(instruction[7:10],instruction[10:13],instruction[13:])

    elif instruction[:5] == '00010':
        moveImmediate(instruction[5:8],instruction[8:])

    elif instruction[:5] == '00011':
        moveRegister(instruction[10:13],instruction[13:])

    elif instruction[:5] == '00100':
        load(instruction[5:8],instruction[8:])

    elif instruction[:5] == '00101':
        store(instruction[5:8],instruction[8:])

    elif instruction[:5] == '00110':
        mul(instruction[7:10],instruction[10:13],instruction[13:])

    elif instruction[:5] == '00111':
        div(instruction[10:13],instruction[13:])

    elif instruction[:5] == '01000':
        rightShift(instruction[5:8],instruction[8:])

    elif instruction[:5] == '01001':
        leftShift(instruction[5:8],instruction[8:])

    elif instruction[:5] == '01010':
        xor(instruction[7:10],instruction[10:13],instruction[13:])

    elif instruction[:5] == '01011':
        Or(instruction[7:10],instruction[10:13],instruction[13:])

    elif instruction[:5] == '01100':
        And(instruction[7:10],instruction[10:13],instruction[13:])

    elif instruction[:5] == '01101':
        invert(instruction[10:13],instruction[13:])

    elif instruction[:5] == '01110':
        compare(instruction[10:13],instruction[13:])

    elif instruction[:5] == '01111':
        jmp(instruction[8:])

    elif instruction[:5] == '10000':
        jlt(instruction[8:])

    elif instruction[:5] == '10001':
        jgt(instruction[8:])

    elif instruction[:5] == '10010':
        je(instruction[8:])


cycle = 0
cycle_number = []
instruction_number = []

while PC < len(MEM):
    instruction = MEM[PC]

    cycle_number.append(cycle)
    instruction_number.append(PC)

    if instruction[:5] == '00011' or instruction[:5] == '01111' or instruction[:5] == '10000' or instruction[:5] == '10001' or instruction[:5] == '10010':
        FLAGS = FLAGS
    else:
        FLAGS = '0000000000000000'

    if instruction[:5] == '10011':
        print(decimalToBinary8(PC) + ' ' + R0 + ' ' + R1 + ' ' + R2 + ' ' + R3 + ' ' + R4 + ' ' + R5 + ' ' + R6 + ' ' + FLAGS)
        break

    execute(instruction, PC)
    print(decimalToBinary8(PC) + ' ' + R0 + ' ' + R1 + ' ' + R2 + ' ' + R3 + ' ' + R4 + ' ' + R5 + ' ' + R6 + ' ' + FLAGS)
    PC += 1
    cycle += 1

#MEM dump
for line in MEM:
    print(line)


#BONUS
#--------------------------------------------------------------------------------------------------------------

def memoryAccessTrace():
    plt.scatter(cycle_number, instruction_number)
    plt.plot(cycle_number, instruction_number)
    plt.xlabel('Cycle')
    plt.ylabel('Address')
    plt.savefig('plot.png')

memoryAccessTrace()