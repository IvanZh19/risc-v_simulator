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
    parse_tree = parse_lines(tokenized_lines)
    print(parse_tree)
