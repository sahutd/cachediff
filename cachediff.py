class AssemblyLine:
    '''
    An abstract representation of an assembly instruction
    '''
    def __init__(self, assembly_line):
        '''
        assembly_line - a line in an assembly instruction
        '''
        self.assembly_line = '0x'+assembly_line[0:6]

    def get_virtual_address(self):
        '''
        return virtual address corresponding to line
        '''
        return int(self.assembly_line,16)


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
        for instr in assembly_instructions.split('\n'):
            if len(instr) >7 and instr.strip()[0:6].isalnum():
                self.assembly_instructions.append('0x'+instr.strip()[0:6])

    def get_virtual_addresses(self):
        '''
        return set containing all virtual addresses for instruction
        '''
        return set([int(i,16) for i in self.assembly_instructions])

    def has_virtual_address(self, address):
        '''
        address - a virtual space address
        return - bool true if address corresponds to an
                 assembly instruction for this instruction
        '''
        return hex(address) in self.assembly_instructions


class File:
    '''
    An abstract representation of a C/C++ file.
    '''
    def __init__(self, filename):
        '''
        filename - absolute path to file
        '''
        self.filename = filename

    def get_high_level_lines(self):
        '''
        @return Line objects corresponding to each high level
        line in file
        '''
        pass

    def get_line_count(self):
        '''
        return - number of high level lines
        '''
        pass

    def get_line(self, virtual_address):
        '''
        return HighLine object coressponding to virtual_address
        '''
        pass
