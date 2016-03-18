import unittest
import unittest.mock
import os
import cachediff


class TestAssemblyInstruction(unittest.TestCase):
    def test_simple(self):
        line = '4005d6:       48 83 c4 08             add    $0x8,%rsp'
        ai = cachediff.AssemblyLine(line)
        self.assertEqual(ai.get_virtual_address(), 0x4005d6)


class TestHighLine(unittest.TestCase):
    def setUp(self):
        lineno = 8
        instructions = '''
         40051a:    c7 45 f8 00 00 00 00    movl   $0x0,-0x8(%rbp)
         400521:  eb 44                   jmp    400567 <main+0x61>
         400563:   83 45 f8 01             addl   $0x1,-0x8(%rbp)
         400567:   83 7d f8 63             cmpl   $0x63,-0x8(%rbp)
         40056b: 7e b6                   jle    400523 <main+0x1d>
        '''
        self.hl = cachediff.HighLine(lineno, instructions)

    def test_get_virtual_addresss(self):
        expected = set([0x40051a, 0x400521, 0x400563, 0x400567,
                       0x40056b, ])
        self.assertEqual(self.hl.get_virtual_addresses(),
                         expected)

    def test_has_virtual_address(self):
        self.assertTrue(self.hl.has_virtual_address(0x40051a))
        self.assertFalse(self.hl.has_virtual_address(0x30051a))


class TestFile(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.getcwd(), 'test_samples',
                                 'test_file.c')
        file_path1 = os.path.join(os.getcwd(), 'test_samples',
                                  'qsort.c')
        dumpfile = os.path.join(os.getcwd(), 'test_samples',
                                'test_file_dump.dump')
        dumpfile1 = os.path.join(os.getcwd(), 'test_samples',
                                 'qsort_dump.dump')
        test_prefix = '/home/saimadhav/cachediff/test_samples/'
        self.f = cachediff.File(file_path, dumpfile,
                                test_prefix+'test_file.c')
        self.f1 = cachediff.File(file_path)
        self.f2 = cachediff.File(file_path1, dumpfile1,
                                 test_prefix+'qsort.c')

    def test_get_high_level_lines(self):
        temp = self.f.get_high_level_lines()
        self.assertEqual(len(temp), self.f.get_line_count())
        # temp[0] corresponds to line3 in test_file_dump.dump
        self.assertTrue(temp[0].has_virtual_address(0x400506))

    def test_get_line_count(self):
        self.assertEqual(self.f.get_line_count(), 5)  # see test_file_dump.dump
        self.assertEqual(self.f2.get_line_count(), 13)

    def test_get_line(self):
        hl = self.f.get_line(0x400506)
        self.assertEqual(hl.lineno, 3)
        hl = self.f.get_line(0x400523)
        self.assertEqual(hl.lineno, 10)
        with self.assertRaises(ValueError):
            hl = self.f.get_line(0x400580)
        with self.assertRaises(ValueError):
            hl = self.f.get_line(0x123456)

        hl = self.f2.get_line(0x4006e4)
        self.assertEqual(hl.lineno, 20)


class TestRun(unittest.TestCase):
    def setUp(self):
        self.run = unittest.mock.Mock()
        self.run.transform_trace_file = cachediff.Run.transform_trace_file
        self.pintrace = os.path.join(os.getcwd(), 'test_samples',
                                     'pintrace.out')


class TestResult(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.getcwd(), 'test_samples',
                            'dinero_output')
        self.result = cachediff.Result(path)
        self.result1 = cachediff.Result(path)

    def test_diff(self):
        parm = ['l1_icache_instrn_fetches',
                'l1_dcache_read_fetches',
                'l1_icache_instrn_miss_rate',
                'l2_ucache_misses',
                'l3_ucache_bytes_to_memory']
        tmp = self.result.get_diff(self.result1, parm)
        for i in tmp.values():
            self.assertEqual(i, 0)

        with self.assertRaises(ValueError):
            tmp = self.result.get_diff(self.result1, ['ABC'])

    def test_simple(self):
        results = self.result.results

        self.assertEqual(results['l1_icache_instrn_fetches'], 215903)
        self.assertEqual(results['l1_icache_instrn_misses'], 814)
        self.assertEqual(results['l1_icache_instrn_miss_rate'], 0.0038)
        self.assertEqual(results['l1_icache_bytes_from_memory'], 52096)
        self.assertEqual(results['l1_dcache_data_fetches'], 79157)
        self.assertEqual(results['l1_dcache_read_fetches'], 55538)
        self.assertEqual(results['l1_dcache_write_fetches'], 23619)
        self.assertEqual(results['l1_dcache_data_misses'], 3109)
        self.assertEqual(results['l1_dcache_read_misses'], 2548)
        self.assertEqual(results['l1_dcache_write_misses'], 561)
        self.assertEqual(results['l1_dcache_bytes_from_memory'], 198976)
        self.assertEqual(results['l1_dcache_bytes_to_memory'], 42560)
        self.assertEqual(results['l2_ucache_fetches'], 4588)
        self.assertEqual(results['l2_ucache_instrn_fetches'], 814)
        self.assertEqual(results['l2_ucache_data_fetches'], 3774)
        self.assertEqual(results['l2_ucache_read_fetches'], 3109)
        self.assertEqual(results['l2_ucache_misses'], 3218)
        self.assertEqual(results['l2_ucache_instrn_misses'], 811)
        self.assertEqual(results['l2_ucache_data_misses'], 2407)
        self.assertEqual(results['l2_ucache_read_misses'], 2407)
        self.assertEqual(results['l2_ucache_write_misses'], 0)
        self.assertEqual(results['l2_ucache_bytes_from_memory'], 205952)
        self.assertEqual(results['l2_ucache_bytes_to_memory'], 34496)

        self.assertEqual(results['l3_ucache_fetches'], 3757)
        self.assertEqual(results['l3_ucache_instrn_fetches'], 811)
        self.assertEqual(results['l3_ucache_data_fetches'], 2946)
        self.assertEqual(results['l3_ucache_read_fetches'], 2407)
        self.assertEqual(results['l3_ucache_misses'], 3218)
        self.assertEqual(results['l3_ucache_instrn_misses'], 811)
        self.assertEqual(results['l3_ucache_data_misses'], 2407)
        self.assertEqual(results['l3_ucache_read_misses'], 2407)
        self.assertEqual(results['l3_ucache_write_misses'], 0)
        self.assertEqual(results['l3_ucache_bytes_from_memory'], 205952)
        self.assertEqual(results['l3_ucache_bytes_to_memory'], 34496)


class TestSingleContiguousDiff(unittest.TestCase):
    def setUp(self):
        cwd = os.getcwd()
        f1_path = os.path.join(cwd, 'test_samples',
                               'test_file.c')
        f2_path = os.path.join(cwd, 'test_samples',
                               'test_file_one.c')
        f3_path = os.path.join(cwd, 'test_samples',
                               'test_file_two.c')
        f5_path = os.path.join(cwd, 'test_samples',
                               'test_file_three.c')
        self.f1 = cachediff.File(f1_path)
        self.f2 = cachediff.File(f2_path)
        self.f3 = cachediff.File(f3_path)
        self.f4 = cachediff.File(f1_path)
        self.f5 = cachediff.File(f5_path)
        self.diff_one = cachediff.single_contiguous_diff(self.f1,
                                                         self.f2)
        self.diff_two = cachediff.single_contiguous_diff(self.f1,
                                                         self.f4)
        self.diff_three = cachediff.single_contiguous_diff(self.f3,
                                                           self.f5)

    def test_diff_simple(self):
        self.assertEqual(len(self.diff_one[0]), 1)
        self.assertEqual(len(self.diff_one[1]), 1)
        self.assertEqual(self.diff_one[0][0].lineno, 10)
        self.assertEqual(self.diff_one[1][0].lineno, 10)

        self.assertEqual(len(self.diff_three[0]), 1)
        self.assertEqual(len(self.diff_three[1]), 3)
        self.assertEqual(self.diff_three[1][1].lineno, 5)

    def test_diff_empty(self):
        self.assertEqual(self.diff_two, ([], []))


if __name__ == '__main__':
    unittest.main()
