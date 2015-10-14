import unittest
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


if __name__ == '__main__':
    unittest.main()
