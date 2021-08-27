#Done By
#Vishwesh Vhavle, 2020156
#Dev Thakkar, 2020052
#Sahil Deshpande, 2020114

import operations
import errors
from sys import stdin

#OPCODES
# add 00000 | sub 00001 | mov $Imm 00010 | mov 00011 | ld 00100 | st 00101
# mul 00110 | div 00111 | rs 01000 | ls 01001 | xor 01010 | or 01011 | and 01100
# not 01101 | cmp 01110 | jmp 01111 | jlt 10000 | jgt 10001 | je 10010 | hlt 10011

#-----------------------------------------------------------------------------------

variables = []

#Storing stdin inputs of assembly code in array
assembly_code = []
machine_code = []
for line in stdin:
    if line == '':
        break
    else:
        assembly_code.append(line.split())

line_number = 0
memory_count = 0
output = True
labels = []

assembly_code, labels = operations.assembly_code_builder(assembly_code)

#Removes Empty Lines
for i in range(len(assembly_code)-1,-1,-1):
    if assembly_code[i] == []:
        assembly_code.pop(i)

hlt_count = 0
line_number = 1

for line in assembly_code:
    if line[0] == 'hlt':
        hlt_count += 1
        if hlt_count > 1:
            print("Multiple instance of hlt instruction, Line", line_number)
            output = False
            break
    line_number += 1

line_number = 1
variable_truth = 1

variable_count = 0

for line in assembly_code:
    if line[0] == 'var':
        variable_count += 1


if assembly_code[-1][0] == 'hlt':
    for line in assembly_code:
        if line[0] == 'var':
            if variable_truth == 1:
                error = errors.error_type_Var(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    variables.append(line[1])
                    variables.append(len(assembly_code)-variable_count+memory_count)
                    memory_count += 1
            elif variable_truth == 0:
                print('Variables not declared in the beginning, Line',line_number)
                output = False
                break

        elif line[0] != 'var':
            variable_truth = 0

            if line[0] == 'add':
                error = errors.error_type_A(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.add(line[1],line[2],line[3],line_number))

            elif line[0] == 'sub':
                error = errors.error_type_A(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.sub(line[1],line[2],line[3],line_number))

            elif line[0] == 'mov':
                if line[2][0] == '$':
                    error = errors.error_type_B(line)
                    if error[0] == True:
                        print(error[1] + ', Line', line_number)
                        output = False
                        break
                    else:
                        machine_code.append(operations.moveImmediate(line[1],line[2][1:],line_number))
                else:
                    error = errors.error_type_C(line)
                    if error[0] == True:
                        print(error[1] + ', Line', line_number)
                        output = False
                        break
                    else:
                        machine_code.append(operations.moveRegister(line[1],line[2],line_number))

            elif line[0] == 'ld':
                error = errors.error_type_D(line,variables,labels)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.load(line[1],line[2],line_number,variables))

            elif line[0] == 'st':
                error = errors.error_type_D(line,variables,labels)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.store(line[1],line[2],line_number,variables))

            elif line[0] == 'mul':
                error = errors.error_type_A(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.mul(line[1],line[2],line[3],line_number))

            elif line[0] == 'div':
                error = errors.error_type_C(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.div(line[1],line[2],line_number))

            elif line[0] == 'rs':
                error = errors.error_type_B(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.rightShift(line[1],line[2][1:],line_number))

            elif line[0] == 'ls':
                error = errors.error_type_B(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.leftShift(line[1],line[2][1:],line_number))

            elif line[0] == 'xor':
                error = errors.error_type_A(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.xor(line[1],line[2],line[3],line_number))

            elif line[0] == 'or':
                error = errors.error_type_A(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.Or(line[1],line[2],line[3],line_number))

            elif line[0] == 'and':
                error = errors.error_type_A(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.And(line[1],line[2],line[3],line_number))

            elif line[0] == 'not':
                error = errors.error_type_C(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.invert(line[1],line[2],line_number))

            elif line[0] == 'cmp':
                error = errors.error_type_C(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.compare(line[1],line[2],line_number))

            elif line[0] == 'jmp':
                error = errors.error_type_E(line, labels, variables)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.jmp(line[1],line_number))

            elif line[0] == 'jlt':
                error = errors.error_type_E(line, labels, variables)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.jlt(line[1],line_number))

            elif line[0] == 'jgt':
                error = errors.error_type_E(line, labels, variables)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.jgt(line[1],line_number))

            elif line[0] == 'je':
                error = errors.error_type_E(line, labels, variables)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.je(line[1],line_number))

            elif line[0] == 'hlt':
                error = errors.error_type_F(line)
                if error[0] == True:
                    print(error[1] + ', Line', line_number)
                    output = False
                    break
                else:
                    machine_code.append(operations.hlt())

        #memory_count += 1
        line_number += 1

    if output == True:
        #stdout Machine Code Output
        for line in machine_code:
            print(line)

else:
    print("Instructions do not terminate with an hlt, Line", len(assembly_code))