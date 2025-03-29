# initialize the register names and symbolic names
symbolic_names = ['zero','ra','sp','gp','tp','t0','t1','t2','s0','s1',
                   'a0','a1','a2','a3','a4','a5','a6','a7',
                   's2','s3','s4','s5','s6','s7','s8','s9','s10','s11',
                   't3','t4','t5','t6']
register_numbers = {}
for i in range(32):
    register_numbers[f'x{i}'] = i
    register_numbers[symbolic_names[i]] = i

class Instruction:
    def __init__(self, instr_type, arg1=None, arg2=None, arg3=None):
        self.instr_type = instr_type
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

class Memory:
    """
    Represents a virtual memory space for memory access instructions.
    RISC-V uses byte addressing, and we assume a 32-bit CPU.
    This means to access the next word in memory, we add 4 to the address.
    We can theoretically hold 2^30 different words.
    For this purpose, there is also no need for a cache abstraction.
    """
    def __init__(self):
        self.memory = {}

    def get_value(self, addr):
        assert addr <= 0xffffffff, 'addr out of bounds'
        return self.memory[addr] if addr in self.memory.keys() else 0x0

    def store_value(self, addr, value):
        assert addr <= 0xffffffff, 'addr out of bounds'
        self.memory[addr] = value

    def clear(self):
        self.memory = {}

    def display(self):
        # TODO: improve formatting later
        print(self.memory)

class Process:
    """
    Represents a process, with 32 registers each 32 bits large.
    Registers may be referred to by symbolic names, or just x0-x31.
    Acts on a virtual memory space.
    """
    def __init__(self, instructions, labels, memory):
        """
        instructions is a list of Instructions,
        labels is a dict mapping string label names to list indices in instructions.
        memory is a Memory object that this Process will interact with.
        """
        self.registers = [0x0 for i in range(32)]
        self.instructions = instructions
        self.labels = labels
        self.memory = memory
        self.pc = 0x0

    def execute(self, instr):
        arg1_reg_num = register_numbers[instr.arg1] if instr.arg1 in register_numbers.keys() else 0
        arg2_reg_num = register_numbers[instr.arg2] if instr.arg2 in register_numbers.keys() else 0
        arg3_reg_num = register_numbers[instr.arg3] if instr.arg3 in register_numbers.keys() else 0
        match instr.instr_type:
            case 'lui':
                self.registers[arg1_reg_num] = int(instr.arg2, 16) << 12
            case 'jal':
                self.registers[arg1_reg_num] = self.pc + 0x4
                self.pc = self.labels[instr.arg2]
            case 'jalr':
                self.registers[arg1_reg_num] = self.pc + 0x4
                # TODO: parse offset(rs1) to update pc
            case 'beq':
                branch = (self.registers[arg1_reg_num] == self.registers[arg2_reg_num])
                self.pc = self.labels[instr.arg3] * 4 if branch else self.pc + 0x4
            case 'bne':
                branch = (self.registers[arg1_reg_num] != self.registers[arg2_reg_num])
                self.pc = self.labels[instr.arg3] * 4 if branch else self.pc + 0x4
            case 'blt':
                branch = (self.registers[arg1_reg_num] < self.registers[arg2_reg_num])
                self.pc = self.labels[instr.arg3] * 4 if branch else self.pc + 0x4
            case 'bge':
                branch = (self.registers[arg1_reg_num] >= self.registers[arg2_reg_num])
                self.pc = self.labels[instr.arg3] * 4 if branch else self.pc + 0x4
            case 'bltu':
                branch = (self.registers[arg1_reg_num] < self.registers[arg2_reg_num])
                self.pc = self.labels[instr.arg3] * 4 if branch else self.pc + 0x4
                # TODO: handle signed and unsigned operations, this and bgeu
            case 'bgeu':
                branch = (self.registers[arg1_reg_num] >= self.registers[arg2_reg_num])
                self.pc = self.labels[instr.arg3] * 4 if branch else self.pc + 0x4
            case 'lb':
                pass
            case 'lh':
                pass
            case 'lw':
                pass
            case 'lbu':
                pass
            case 'lhu':
                pass
            case 'sb':
                pass
            case 'sh':
                pass
            case 'sw':
                pass
            case 'addi':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] + int(instr.arg3, 0)
            case 'slti':
                pass
            case 'sltiu':
                pass
            case 'xori':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] ^ int(instr.arg3, 0)
            case 'ori':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] | int(instr.arg3, 0)
            case 'andi':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] & int(instr.arg3, 0)
            case 'slli':
                pass
            case 'srli':
                pass
            case 'srai':
                pass
            case 'add':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] + self.registers[arg3_reg_num]
            case 'sub':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] - self.registers[arg3_reg_num]
            case 'sll':
                pass
            case 'slt':
                pass
            case 'sltu':
                pass
            case 'xor':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] ^ self.registers[arg3_reg_num]
            case 'srl':
                pass
            case 'sra':
                pass
            case 'or':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] | self.registers[arg3_reg_num]
            case 'and':
                self.registers[arg1_reg_num] = self.registers[arg2_reg_num] & self.registers[arg3_reg_num]
            case _:
                raise Exception('unsupported operation')







def tokenize_with_line_grouping(filename):
    """
    Returns a list of lists, each of which has all of the tokens on that line,
    using a base set of RISC-V assembly instructions.
    """
    with open(filename, 'r') as file:
        raw_text = file.read()
    lines = raw_text.split('\n')
    tokenized_lines = []
    for line in lines:
        tokenized_line = []
        tokens = line.split(' ')
        for token in tokens:
            if token == '':
                continue
            if token == '#':
                break
            elif token[-1] == ',':
                tokenized_line.append(token[:-1])
            else:
                tokenized_line.append(token)
        if tokenized_line != []:
            tokenized_lines.append(tokenized_line)
    return tokenized_lines

def parse_lines(tokenized_lines):
    """
    Constructs a list of Instructions representing the instructions in tokenized_lines.
    Also constructs a dictionary mapping label names to indices of the list of Instructions.
    Returns a tuple of the list and dictionary.
    """
    instructions = []
    labels = {}
    line_ix = 0
    for line in tokenized_lines:
        match len(line):
            case 1:
                assert line[0][-1] == ':', 'incorrect label syntax'
                labels[line[0][:-1]] = line_ix
            case 3 | 4:
                instr = Instruction(*line)
                line_ix += 1
                instructions.append(instr)
    return instructions, labels











if __name__=='__main__':
    tokenized_lines = tokenize_with_line_grouping('src.asm')
    print(tokenized_lines)
    instructions, labels = parse_lines(tokenized_lines)
    memory = Memory()
    process = Process(instructions, labels, memory)
    for instr in instructions:
        process.execute(instr)
        print(process.registers)
