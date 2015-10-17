import unittest
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
        file_path = os.path.join(os.getcwd(), 'test_file.c')
        self.f = cachediff.File(file_path)

    def test_get_high_level_lines(self):
        temp = self.f.get_high_level_lines()
        self.assertEqual(len(temp), self.f.get_line_count())
        # temp[0] corresponds to line3 in test_file_dump.dump
        self.assertTrue(temp[0].has_virtual_address(0x400506))

    def test_get_line_count(self):
        self.assertEqual(self.f.get_line_count(), 5)  # see test_file_dump.dump

    def test_get_line(self):
        hl = self.f.get_line(0x400506)
        self.assertEqual(hl.lineno, 3)
        hl = self.f.get_line(0x400563)
        self.assertEqual(hl.lineno, 8)
        with self.assertRaises(ValueError):
            hl = self.f.get_line(0x400580)
        with self.assertRaises(ValueError):
            hl = self.f.get_line(0x123456)


if __name__ == '__main__':
    unittest.main()
