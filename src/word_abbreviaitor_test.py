import unittest
import word_abbreviator
from parameterized import parameterized

class TestWordSplit(unittest.TestCase):
     
    @parameterized.expand([
        ("Hello World", ['HELLO', 'WORLD']),
        ("I like pancakes", ['I', 'LIKE', 'PANCAKES']),
        ("", [])
    ])       
    def test_split_string_with_normal_cases(self, input_string, expected_result):
        
        actual_result = word_abbreviator.split_string(input_string)
        self.assertEqual(actual_result, expected_result)

    @parameterized.expand([
        ("", []),
        ("Mc`donald Farm's", ['MCDONALD', 'FARMS']),
        ("He%%llo Wo,r;ld", ['HE', 'LLO', 'WO', 'R', 'LD']),
        ('"Hel"lo', ['HEL', 'LO']),
        ("#Speci@l Ch@aracters#", ['SPECI', 'L', 'CH', 'ARACTERS'])
    ])       
    def test_split_string_with_special_cases(self, input_string, expected_result):
        
        actual_result = word_abbreviator.split_string(input_string)
        self.assertEqual(actual_result, expected_result)  
    
    @parameterized.expand([
        (['DOGO'], ['DOG', 'DOO', 'DGO']),
        (['HEL', 'LO'], ['HEL', 'HEL', 'HEO', 'HLL', 'HLO', 'HLO']),
        (['I','LOVE','ME'], ['ILO', 'ILV', 'ILE', 'ILM', 'ILE', 'IOV', 'IOE', 'IOM', 'IOE', 'IVE', 'IVM', 'IVE', 'IEM', 'IEE', 'IME']),
        
    ])      
    def test_find_abbreviations(self, input_string, expected_result):
        
        actual_result = word_abbreviator.find_abbreviations(input_string)
        self.assertEqual(actual_result[0], expected_result)  
        
        
         

if __name__ == '__main__':
    unittest.main()