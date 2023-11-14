import unittest
import word_abbreviator
from parameterized import parameterized

class TestWordSplit(unittest.TestCase):
     
    @parameterized.expand([
        ("Hello World", ['HELLO', 'WORLD']),
        ("I like pancakes", ['I', 'LIKE', 'PANCAKES']),
        ("", [])
    ])       
    def test_split_string_with_normal_string(self, input_string, expected_result):
        
        actual_result = word_abbreviator.split_string(input_string)
        self.assertEqual(actual_result, expected_result)

        

if __name__ == '__main__':
    unittest.main()