class AssemblyLine:
    '''
    An abstract representation of an assembly instruction
    '''
    def __init__(self, assembly_line):
        '''
        assembly_line - a line in an assembly instruction
        '''
        pass

    def get_virtual_address(self):
        '''
        return virtual address corresponding to line
        '''
        pass


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
        pass

    def get_virtual_addresses(self):
        '''
        return set containing all virtual addresses for instruction
        '''
        pass

    def has_virtual_address(self, address):
        '''
        address - a virtual space address
        return - bool true if address corresponds to an
                 assembly instruction for this instruction
        '''
        pass


class File:
    '''
    An abstract representation of a C/C++ file.
    '''
    def __init__(self, filename):
        '''
        filename - absolute path to file
        '''
        pass

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
