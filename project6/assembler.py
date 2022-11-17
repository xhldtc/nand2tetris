import sys
import os


def main():
    asm_name = sys.argv[1]
    full_path = os.path.join(os.getcwd(), asm_name)
    file_name = asm_name[0:asm_name.index(".")]
    output_file = os.path.join(os.getcwd(), file_name+".hack")
    map = init_symbol_dict()
    with open(full_path) as f:
        pc = -1
        for line in f:
            instruction = parse(line)
            if not instruction:
                continue
            if '(' in instruction and ')' in instruction:
                label = instruction[instruction.index('(')+1:instruction.index(')')]
                map[label] = pc+1
            else:
                pc += 1
    
    var_index=16
    with open(output_file, 'w+') as w:
        with open(full_path,'r') as f:
            for line in f:
                instruction = parse(line)
                if not instruction or '(' in instruction:
                    continue
                elif '@' in instruction:
                    command = instruction[1:]
                    if command.isdigit():
                        w.write(code('0', command))
                    elif command in map:
                        w.write(code('0', map[command]))
                    else:
                        map[command] = var_index
                        w.write(code('0', var_index))
                        var_index+=1
                    w.write('\n')
                else:
                    w.write(code('111', instruction) + '\n')


def parse(line):
    line = line.strip()
    comment_start = line.find("//")
    if comment_start != -1:
        line = line[0:comment_start]
    line = line.replace(' ', '')
    return line

def code(typ, command):
    if typ == '0':
        return typ + format(int(command), "015b")
    else:
        jmp = jump_code(command[command.index(';')+1:]) if ';' in command else '000'
        # print(jmp)
        if ';' in command:
            command = command[0:command.index(';')]
        dst = dest_code(command[0:command.index('=')]) if '=' in command else '000'
        # print(dst)
        if '=' in command:
            command = command[command.index('=')+1:]
        # print(command)
        a = '1' if 'M' in command else '0'
        return typ + a + comp_code(command) + dst + jmp


def jump_code(cmd):
    if cmd == 'JGT':
        return '001'
    elif cmd == 'JEQ':
        return '010'
    elif cmd == 'JGE':
        return '011'
    elif cmd == 'JLT':
        return '100'
    elif cmd == 'JNE':
        return '101'
    elif cmd == 'JLE':
        return '110'
    elif cmd == 'JMP':
        return '111'
    else:
        return '000'
    
def dest_code(cmd):
    res=''
    res += '1' if 'A' in cmd else '0'
    res += '1' if 'D' in cmd else '0'
    res += '1' if 'M' in cmd else '0'
    return res

def comp_code(cmd):
    cmap = {}
    cmap['0']= '101010'
    cmap['1']= '111111'
    cmap['-1']= '111010'
    cmap['D']= '001100'
    cmap['A']= '110000'
    cmap['!D']= '001101'
    cmap['!A']= '110001'
    cmap['-D']= '001111'
    cmap['-A']= '110011'
    cmap['D+1']= '011111'
    cmap['A+1']= '110111'
    cmap['D-1']= '001110'
    cmap['A-1']= '110010'
    cmap['D+A']= '000010'
    cmap['D-A']= '010011'
    cmap['A-D']= '000111'
    cmap['D&A']= '000000'
    cmap['D|A']= '010101'
    cmap['M']= cmap['A']
    cmap['!M']= cmap['!A']
    cmap['-M']= cmap['-A']
    cmap['M+1']= cmap['A+1']
    cmap['M-1']= cmap['A-1']
    cmap['D+M']= cmap['D+A']
    cmap['D-M']= cmap['D-A']
    cmap['M-D']= cmap['A-D']
    cmap['D&M']= cmap['D&A']
    cmap['D|M']= cmap['D|A']
    return cmap[cmd]


def init_symbol_dict():
    map = {}
    map['SP'] = 0
    map['LCL'] = 1
    map['ARG'] = 2
    map['THIS'] = 3
    map['THAT'] = 4
    map['R0'] = 0
    map['R1'] = 1
    map['R2'] = 2
    map['R3'] = 3
    map['R4'] = 4
    map['R5'] = 5
    map['R6'] = 6
    map['R7'] = 7
    map['R8'] = 8
    map['R9'] = 9
    map['R10'] = 10
    map['R11'] = 11
    map['R12'] = 12
    map['R13'] = 13
    map['R14'] = 14
    map['R15'] = 15
    map['SCREEN'] = 16384
    map['KBD'] = 24576
    return map


if __name__ == '__main__':
    main()
