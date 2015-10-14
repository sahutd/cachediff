import unittest
import cachediff


class TestAssemblyInstruction(unittest.TestCase):
    def test_simple(self):
        line = '4005d6:       48 83 c4 08             add    $0x8,%rsp'
        ai = cachediff.AssemblyLine(line)
        self.assertEqual(ai.get_virtual_address(), 0x4005d6)



if __name__ == '__main__':
    unittest.main()
