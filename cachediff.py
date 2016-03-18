import sys
import os
import shutil
import re
import subprocess
import collections
import tempfile
import difflib
import logging
import itertools
import time


def getLogger():
    '''
    Return a custom logging object with timestamp
    being measured in seconds since start of process
    '''

    class UnixTimeStampFormatter(logging.Formatter):
        def __init__(self, *args, **kwargs):
            self.epoch = time.time()
            logging.Formatter.__init__(self, *args, **kwargs)

        def formatTime(self, record, datefmt=None):
            return "{0:.3f}s".format(record.created - self.epoch)

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = UnixTimeStampFormatter(
            "%(asctime)s %(levelname)-5.5s  %(message)s"
            )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger = getLogger()


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
    def __init__(self, filename, dumpfile=None,
                 _test_filename_=None):
        '''
        filename - absolute path to file
        '''
        logger.info('START: Creating File() for %s' % filename)
        self.filename = filename
        if dumpfile:
            self.dumpfile = dumpfile
        else:
            self.create_dumpfile()
        self._test_filename_ = _test_filename_
        self.lines = self.init_file()
        self.cleanup(dumpfile=dumpfile)
        logger.info('END: Creating File() for %s' % filename)

    def init_file(self):
        '''
        @return a sorted list of HighLine objects from the given filename
        '''
        with open(self.dumpfile) as f:
            dump = f.readlines()
        if self._test_filename_:
            self.filename = self._test_filename_
        in_line = False
        instruction = collections.OrderedDict()
        for i in dump:
            if not i.strip():
                in_line = False
                continue
            if 'file format' in i:
                continue
            if i.startswith(self.filename):
                in_line = True
                temp = i.split()[0]
                current_lineno = int(temp.split(':')[1])
            elif in_line:
                if not instruction.get(current_lineno):
                    instruction[current_lineno] = ''
                instruction[current_lineno] += '\n' + i
        list_ = []

        for k, v in instruction.items():
            list_.append(HighLine(k, v))
        return list_

    def create_dumpfile(self):
        self.executable = '{}.out'.format(self.filename)
        obj = subprocess.Popen(['gcc', '-g', self.filename, '-o',
                                self.executable])
        obj.wait()
        tmp = tempfile.NamedTemporaryFile(delete=False)
        obj = subprocess.Popen(['objdump', '-dl', self.executable], stdout=tmp)
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

    def cleanup(self, dumpfile):
        if not dumpfile:
            os.remove(self.dumpfile)


class Result:
    '''
    An abstract representation of a DineroIV output
    '''
    def __init__(self, dinero_output):
        '''
        filename = path to dinero_output
        results = dict containing key as cache_type_operation like
        l1_dcache_write_fetch and value as Number (int/float)
        '''
        self.filename = dinero_output
        self.results = self.get_results()

    def get_diff(self, obj_b, list_parameters):
        '''
        @return a dictionary with keys as given list of parameter and
        value as difference btw parameter of both objects
        '''
        res_a = self.results
        res_b = obj_b.results
        tmp = dict()
        for parm in list_parameters:
            if parm in res_a.keys():
                tmp[parm] = res_a[parm] - res_b[parm]
            else:
                raise ValueError

        return tmp

    def get_results(self):
        '''
        @return the dictionay with key as cache_type_operation
        and value as Number (int/float)
        '''
        tmp = []
        with open(self.filename, "r") as f:
            tmp = f.readlines()

        N = len(tmp)
        i = 0
        table_size = 16
        x = dict()
        while i < N:
            if re.match("\w\d-\w+", tmp[i].strip()):
                name = tmp[i].strip().split('-')
                name = '_'.join(name)
                x[name] = list()
                for j in range(1, table_size):
                    if tmp[i+j].strip() != '':
                        x[name].append(tmp[i+j].strip().split())

                i += table_size
            else:
                i += 1

        xy = dict()
        for k, v in x.items():
            headers = ["_"+j.lower() for j in v[0]][1:]
            headers[0] = ""
            for i in [2, 4, 5]:
                row_name = re.findall(('[A-Za-z]+'), ' '.join(v[i]))
                row_name = [j.lower() for j in row_name if j != 'Demand']
                row_nums = []
                if row_name[0] == 'miss':
                    row_nums = re.findall(('\d+\.\d+'), ' '.join(v[i]))
                    row_nums = [float(j) for j in row_nums]
                else:
                    row_nums = re.findall(('\d+'), ' '.join(v[i]))
                    row_nums = [int(j) for j in row_nums]

                row_name = '_'.join(row_name)
                for col in range(len(row_nums)):
                    xy[k+headers[col]+"_"+row_name] = row_nums[col]

            for i in [7, 9]:
                row_name = [j.lower() for j in re.findall(('[A-Za-z]+'),
                            ' '.join(v[i]))]
                row_nums = [int(j) for j in re.findall(('\d+'),
                            ' '.join(v[i]))]

                row_name = '_'.join(row_name)
                for col in range(len(row_nums)):
                    xy[k+"_"+row_name] = row_nums[col]

        return xy


class Run:
    '''
    Class to hold all results of a run
    '''
    def __init__(self, sourcefile, inputfile, diff_block):
        logger.info('START: Creating Run() for %s' % sourcefile.filename)
        self.sourcefile = sourcefile
        self.inputfile = inputfile
        self.diff_block = diff_block
        self._pintrace = self.run()
        self.global_cache_result = self.cache_simulate('global')
        self.local_cache_result = self.cache_simulate('local')
        self.global_cache_result = Result(self.global_cache_result)
        self.local_cache_result = Result(self.local_cache_result)
        logger.info('END: Run() for %s' % sourcefile.filename)

    def run(self):
        logger.info('START: Running executable for %s under PIN' %
                    self.sourcefile.filename)
        try:
            pin = os.environ['PIN']
        except:
            raise EnvironmentError('Ensure $PIN is set')
        pin_executable = os.path.join(pin, './pin.sh')
        tracer = os.path.join(pin, 'source', 'tools', 'MyPinTool',
                              'obj-intel64', 'MyPinTool.so')
        stdin = open(self.inputfile)
        p = subprocess.Popen([pin_executable, '-injection', 'child', '-t',
                              tracer,
                              '--',
                              self.sourcefile.executable],
                             stdin=stdin,
                             stdout=tempfile.NamedTemporaryFile())
        p.wait()
        trace_file = tempfile.NamedTemporaryFile().name
        shutil.move('pinatrace.out', trace_file)
        logger.info('END: Running executable for %s under PIN' %
                    self.sourcefile.filename)
        return trace_file

    def cache_simulate(self, locality):
        '''
        locality - 'local' or 'global'
                   if 'local' consider only block given by self.diff_block
                   if 'global' consider entire file
        return Result object corresponding to cache simulator run
        '''
        logger.info('START: %s simulation for %s' %
                    (locality, self.sourcefile.filename))
        if locality == 'local':
            trace_file = self._get_nonlocal_trace_file()
        elif locality == 'global':
            trace_file = self._pintrace
        processor = {'-l1-isize': '64k', '-l1-dsize': '16k',
                     '-l1-ibsize': '64', '-l1-dbsize': '64',
                     '-l1-iassoc': '2', '-l1-dassoc': '4',
                     '-l2-usize': '1024k', '-l2-ubsize': '64',
                     '-l2-uassoc': '16', '-l3-usize': '8192k',
                     '-l3-ubsize': '64', '-l3-uassoc': '16',
                     '-l1-dwback': 'a', }
        try:
            dinero = os.environ['DINERO']
        except:
            raise EnvironmentError('ensure $DINERO is set')
        with open(trace_file) as input_file:
            argument = ' '.join(['{} {}'.format(k, v) for (k, v) in
                                 processor.items()])
            dinero = os.path.join(dinero, 'dineroIV')
            command = [dinero + ' ' + argument + ' -informat d']
            stdout = tempfile.NamedTemporaryFile(delete=False)
            p = subprocess.Popen(command, shell=True, stdin=input_file,
                                 stdout=stdout)
            p.wait()
            logger.info('END: %s simulation for %s' %
                        (locality, self.sourcefile.filename))
            return stdout.name

    def _get_nonlocal_trace_file(self):

        def grouper(iterable, n, fillvalue=None):
            "Collect data into fixed-length chunks or blocks"
            # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
            args = [iter(iterable)] * n
            return itertools.zip_longest(*args, fillvalue=fillvalue)

        logger.info('START: generate local trace for %s' %
                    self.sourcefile.filename)
        pintrace = self._pintrace
        local_trace = tempfile.NamedTemporaryFile(delete=False).name
        local_virtual_addresses = set()
        for d in self.diff_block:
            for address in d.get_virtual_addresses():
                local_virtual_addresses.add(hex(address))
        with open(pintrace) as f, open(local_trace, 'w') as out:
            part1 = ''
            part2 = []
            trace = f.readlines()
            for instrn_trace, mem_trace in grouper(trace, 2):
                ip = instrn_trace.split()[1]
                if ip not in local_virtual_addresses:
                    part1 += mem_trace
                    part1 += instrn_trace

            for mem_trace, instrn_trace in grouper(trace[::-1], 2):
                ip = instrn_trace.split()[1]
                if ip not in local_virtual_addresses:
                    part2.append(mem_trace)
                    part2.append(instrn_trace)
                else:
                    break
            part2 = ''.join(part2[::-1])
            out.write(part1)
            out.write(part2)
        logger.info('END: generate local trace for %s' %
                    self.sourcefile.filename)
        return local_trace


def single_contiguous_diff(file1, file2):
    '''
    return a tuple(x, y)
    where x is the highlines coressponding  to changed blockin file1
    where y is the highlines coressponding to changed block in file2
    '''
    def get_diff_lineno(filename1, filename2):
        '''
        return tuple(x,y) where x and y are list containing the lineno of after
        diffing file1 and file2
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

        return (list_one, list_two)
    tmp = get_diff_lineno(file1.filename, file2.filename)

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
            list_file1.append(HighLine(lineno, ""))
        else:
            list_file1.append(dict_file1[lineno])

    for lineno in tmp[1]:
        if lineno not in dict_file2.keys():
            list_file2.append(HighLine(lineno, ""))
        else:
            list_file2.append(dict_file2[lineno])
    return (list_file1, list_file2)


def perform_analysis(run1, run2):
    '''
    Statistical Analysis between run1 and run2
    @return A Multiline string containing the Statistics of run1 and run2
    '''
    def _get_cache_output(run1, run2, cache_type, parm=[]):
        '''
        @return Statistical Analysis for a particular type of cache
        '''
        logger.info('START: result Analysis')
        result_l1 = run1.local_cache_result.results
        result_l2 = run2.local_cache_result.results
        result_g1 = run1.global_cache_result.results
        result_g2 = run2.global_cache_result.results
        result_string = []
        if cache_type == 'l1_dcache_':
            result_string.append('L1 - DATA CACHE')
            if not parm:
                parm = [
                        'fetches',
                        'misses',
                        # 'miss_rate',
                        'bytes_from_memory',
                        'bytes_to_memory'
                        ]
        elif cache_type == 'l1_icache_':
            result_string.append('L1 - INSTRUCTION CACHE')
            if not parm:
                parm = [
                        'fetches',
                        'misses',
                        # 'miss_rate',
                        'bytes_from_memory',
                        'bytes_to_memory'
                        ]
        elif cache_type == 'l2_ucache_':
            result_string.append('L2 - UNIFIED CACHE')
            if not parm:
                parm = [
                        'fetches',
                        'misses',
                        'instrn_fetches',
                        'instrn_misses',
                        'data_fetches',
                        'data_misses',
                        # 'miss_rate',
                        'bytes_from_memory',
                        'bytes_to_memory'
                        ]
        elif cache_type == 'l3_ucache_':
            result_string.append('L3 - UNIFIED CACHE')
            if not parm:
                parm = [
                        'fetches',
                        'misses',
                        'instrn_fetches',
                        'instrn_misses',
                        'data_fetches',
                        'data_misses',
                        # 'miss_rate',
                        'bytes_from_memory',
                        'bytes_to_memory'
                        ]

        max_ = max([len(i) for i in parm])
        max_space = ' ' * (max_ + 3)
        x = max_space+'LOCAL FILE1'+' '*(max_ - len('LOCAL FILE1')) + \
            'LOCAL FILE2'
        x += ' '*(max_ - len('LOCAL FILE2'))+'GLOBAL FILE1'
        x += ' '*(max_ - len('GLOBAL FILE1'))+'GLOBAL FILE2'
        result_string.append(x)

        for p in parm:
            title = ' '.join(p.split('_')).upper() + \
                            ' '*(max_ - len(p))+' : '
            temp = cache_type + p
            if 'rate' in temp:
                val1 = result_l1[temp]
                val2 = result_l2[temp]
            else:
                val1 = result_g1[temp] - result_l1[temp]
                val2 = result_g2[temp] - result_l2[temp]
            val3 = result_g1[temp]
            val4 = result_g2[temp]
            val1, val2, val3, val4 = list(map(abs, [val1, val2, val3, val4]))
            x = title+str(val1)+' '*(max_ - len(str(val1)))+str(val2)
            x += ' '*(max_ - len(str(val2)))+str(val3)
            x += ' '*(max_ - len(str(val3)))+str(val4)
            result_string.append(x)

        result_string.append('\n\n\n')

        return '\n'.join(result_string)

    result_string = '----------LOCAL AND GLOBAL CACHE ANALYSIS----------\n'
    result_string += _get_cache_output(run1, run2, 'l1_dcache_')
    result_string += _get_cache_output(run1, run2, 'l1_icache_')
    result_string += _get_cache_output(run1, run2, 'l2_ucache_')
    result_string += _get_cache_output(run1, run2, 'l3_ucache_')

    logger.info('END: result Analysis')

    return result_string


def process(file1, file2, input1, input2):
    '''
    file1 and file2 are input C/C++ files
    input1 and input2 are the input stream to be fed to executables
    of file1 and file2
    return - an object of ResultDiff
    '''
    logger.info('START: Process %s %s' % (file1, file2))
    file1 = File(file1)
    file2 = File(file2)
    diff1, diff2 = single_contiguous_diff(file1, file2)
    run1 = Run(file1, input1, diff1)
    run2 = Run(file2, input2, diff2)
    result = perform_analysis(run1, run2)
    logger.info('END: Process %s %s' % (file1, file2))
    return result


if __name__ == '__main__':
    file1, file2, input1, input2 = sys.argv[1:5]
    file1 = os.path.abspath(file1)
    file2 = os.path.abspath(file2)
    result = process(file1, file2, input1, input2)
    print(result)
