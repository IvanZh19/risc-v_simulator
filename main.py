class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class InstructionNode:
    def __init__(self, addr, next_instr, label=None, val=0, arg1=None, arg2=None, arg3=None):
        self.addr = addr
        self.next_instr = next_instr
        self.label = label
        self.val = val
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

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
    Constructs a "tree" of InstructionNodes representing the instructions in tokenized_lines.
    Note that the arguments "children" of each instruction are simply the primitive values,
    not other Node objects. Returns the head, which is the address of the first line.
    """
    line_addr = 0x0
    line_label = None
    head = None
    num_lines = len(tokenized_lines)
    for line_ix in range(num_lines):
        line = tokenized_lines[line_ix]
        next_instr = None if line_ix == num_lines - 1 else tokenized_lines[line_ix+1]
        match len(line):
            case 1:
                assert line[0][-1] == ':', 'incorrect comment syntax'
                line_label = line[0]
            case 3:
                instr = InstructionNode(line_addr, next_instr, line_label,
                                        line[0], line[1], line[2])
                if line_addr == 0x0:
                    head = instr
                line_addr += 0x4
            case 4:
                instr = InstructionNode(line_addr, next_instr, line_label,
                                        line[0], line[1], line[2], line[3])
                if line_addr == 0x0:
                    head = instr
                line_addr += 0x4
            case _:
                print(len(line))
                raise Exception('incorrect line syntax')
    return head












if __name__=='__main__':
    tokenized_lines = tokenize_with_line_grouping('src.asm')
    print(tokenized_lines)
    parse_tree = parse_lines(tokenized_lines)
    print(parse_tree)
