import re
import subprocess
import tempfile
import difflib


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
        assembly_instructions = [i.strip() for i in
                                 assembly_instructions.split('\n')
                                 if i.strip()]
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



class File:
    '''
    An abstract representation of a C/C++ file.
    '''
    def __init__(self, filename, dumpfile=None):
        '''
        filename - absolute path to file
        '''
        self.filename = filename
        if dumpfile:
            self.dumpfile = dumpfile
        else:
            self.create_dumpfile()
        self.lines = self.init_file()

    def init_file(self):
        '''
        @return a sorted list of HighLine objects from the given filename
        '''
        path = self.filename
        filename = re.findall(r'/.*/(\w+\.\w+)', path)[0]
        dumpfile = self.dumpfile
        is_read = False
        instr = dict()
        line_no = 0
        f = open(dumpfile, 'r')
        x = f.readlines()
        f.close()
        for line in x:
            if is_read and line == '\n':
                break
            tmp = re.findall('/.*/'+filename+':(\d+)', line)
            if tmp:
                is_read = True
                line_no = tmp[0]
                if line_no not in instr.keys():
                    instr[line_no] = []
            elif is_read:
                inst = re.findall('.*', line)
                if inst:
                    instr[line_no].append(inst[0])

        list_ = []
        for i, j in instr.items():
            list_.append(HighLine(int(i), '\n'.join(j)))
        list_.sort(key=lambda x: x.lineno)
        return list_

    def create_dumpfile(self):
        obj = subprocess.Popen(['gcc','-g',self.filename])
        obj.wait()
        tmp = tempfile.NamedTemporaryFile(delete=False)
        obj = subprocess.Popen(['objdump','-dl','./a.out'],stdout = tmp)
        obj.wait()
        self.dumpfile = tmp.name


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
            if virtual_address in obj.assembly_instructions:
                return obj

        raise ValueError


def get_diff_lineno(filename1, filename2):
    '''
    return tuple(x,y) where x and y are list containing the lineno of after diffing file1 and file2
    '''
    fA = open(filename1, "rt")
    fB = open(filename2, "rt")
    fileA = fA.readlines()
    fileB = fB.readlines()
    fA.close()
    fB.close()

    d = difflib.Differ()
    diffs = d.compare(fileA, fileB)
    lineNum_one = 0
    lineNum_two = 0
    list_one = []
    list_two = []

    for line in diffs:
        code = line[:2]
        if code in ("  ",):
            lineNum_one += 1
            lineNum_two += 1
        elif code in ("- ",):
            lineNum_one += 1
            list_one.append(lineNum_one)
        elif code in ("+ ",):
            lineNum_two += 1
            list_two.append(lineNum_two)

    return (list_one,list_two)

def single_contiguous_diff(file1, file2):
    '''
    return a tuple(x, y)
    where x is the highlines coressponding  to changed blockin file1
    where y is the highlines coressponding to changed block in file2
    '''
    tmp = get_diff_lineno(file1.filename,file2.filename)

    # check if more than one block is changed
    if tmp[0]:
        counter = tmp[0][0]
        for i in tmp[0]:
            if i != counter:
                raise ValueError
            else:
                counter += 1
    if tmp[1]:
        counter = tmp[1][0]
        for i in tmp[1]:
            if i != counter:
                raise ValueError
            else:
                counter += 1

    list_file1 = []
    list_file2 = []
    dict_file1 = dict()
    dict_file2 = dict()

    for obj in file1.lines:
        dict_file1[obj.lineno] = obj

    for obj in file2.lines:
        dict_file2[obj.lineno] = obj

    for lineno in tmp[0]:
        if lineno not in dict_file1.keys():
            list_file1.append(HighLine(-1,""))
        else:
            list_file1.append(dict_file1[lineno])

    for lineno in tmp[1]:
        if lineno not in dict_file2.keys():
            list_file2.append(HighLine(-2,""))
        else:
            list_file2.append(dict_file2[lineno])

    return (list_file1, list_file2)
