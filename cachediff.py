class AssemblyLine:
    '''
    An abstract representation of an assembly instruction
    '''
    def __init__(self, assembly_line):
        '''
        assembly_line - a line in an assembly instruction
        '''
        self.assembly_line = '0x' + assembly_line.split()[0][:-1]

    def get_virtual_address(self):
        '''
        return virtual address corresponding to line
        '''
        return int(self.assembly_line, 16)


class HighLine:
    '''
    An abstract representation of a high level C/C++ line
    '''
    def __init__(self, lineno, assembly_instructions):
        '''
        lineno - integer
        assembly_instructions - list of assembly instruction
                               corresponding to line
        '''
        self.lineno = lineno
        self.assembly_instructions = []
        assembly_instructions = [i.strip() for i in assembly_instructions.split('\n') if i.strip()]
        for i in assembly_instructions:
            temp = AssemblyLine(i)
            self.assembly_instructions.append(temp.get_virtual_address())

    def get_virtual_addresses(self):
        '''
        return set containing all virtual addresses for instruction
        '''
        return set([i for i in self.assembly_instructions])

    def has_virtual_address(self, address):
        '''
        address - a virtual space address
        return - bool true if address corresponds to an
                 assembly instruction for this instruction
        '''
        return address in self.assembly_instructions


def init_file(path):
    '''
    @return a sorted list of HighLine objects from the given filename
    NOTE : the logic can be made simpler using proper REGEX
    '''
    import re
    f = open('test_file_dump.dump','r')
    x = f.readlines()
    f.close()
    p = re.compile(path+'.*(?! )')
    is_read = False
    instr = dict()
    line_no = 0
    for line in x:
        if is_read and line == '\n':
            break
        tmp = re.findall(path+':(\d+)',line)
        if tmp:
            is_read = True
            line_no = tmp[0]
            if line_no not in instr.keys():
                instr[line_no] = []
        elif is_read:
            inst = re.findall('.*',line)
            if inst:
                instr[line_no].append(inst[0])

    list_ = []
    for i,j in instr.items():
        list_.append(HighLine(int(i),'\n'.join(j)))
    list_.sort(key=lambda x : x.lineno)
    return list_

class File:
    '''
    An abstract representation of a C/C++ file.
    '''
    def __init__(self, filename):
        '''
        filename - absolute path to file
        '''
        self.filename = filename
        self.lines = init_file(filename)

    def get_high_level_lines(self):
        '''
        @return list of Line objects corresponding to each high level
        line in file
        the list is sorted by HigherLevel file line number
        in ascending order
        '''
        return self.lines

    def get_line_count(self):
        '''
        return - number of high level lines
        '''
        return len(self.lines)

    def get_line(self, virtual_address):
        '''
        return HighLine object coressponding to virtual_address
        '''
        for obj in self.lines:
            if  virtual_address in obj.assembly_instructions:
                return obj

        raise ValueError
