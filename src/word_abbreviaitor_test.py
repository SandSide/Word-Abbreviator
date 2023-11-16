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

    @parameterized.expand([
        ('DOGO', (0,1,2), ['first', 'second', 'third']),
        ('DOGO', (0,1,3), ['first', 'second', 'last']),
        ('DOGO', (0,2,3), ['first', 'third', 'last']),
        ('HELLO#WORLD', (0,4,6), ['first', 'last', 'first']),
        ('HELLO#WORLD', (0,7,10), ['first', 'second', 'last']),
        ('HELLO#WORLD#GOODBYE', (0,3,17), ['first', 'middle', 'middle'])
    ])      
    def test_determine_position_type(self, word, pos, expected_result):
        
        actual_result = word_abbreviator.determine_position_type(pos, word)
        self.assertEqual(actual_result, expected_result)     
    
    @parameterized.expand([
        ([['ABC', 'DEF', 'DEF'], ['GHI', 'AND'], ['FDG']], [['ABC', 'DEF', 'DEF'], ['GHI', 'AND'], ['FDG']]),
        ([['ABC', 'ZAB', 'GHI'], ['GHI', 'JKL'], ['ABC']], [['ZAB'], ['JKL'], []]),
        ([['ABC', 'GHI', 'ABC'], ['GHI', 'AND'], ['FDG', 'AND']], [['ABC', 'ABC'], [], ['FDG']])
    ])      
    def test_remove_duplicate_abbreviations(self, input_string, expected_result):
        
        input_string = [[(y,'') for y in x]for x in input_string]
        expected_result = [[(y,'') for y in x]for x in expected_result]
    
        actual_result = word_abbreviator.remove_duplicate_abbreviations(input_string)
        self.assertEqual(actual_result, expected_result)     
    
        
        
    @parameterized.expand([
        ('DAG', ['first', 'second', 'third'], 37),
        ('POP', ['first', 'first', 'middle'], 11),
        ('MUE', ['first', 'middle', 'last'], 43),
        ('CLD', ['first', 'third', 'last'], 22),
        ('COO', ['first', 'second', 'third'], 43),
        ('CCO', ['first', 'first', 'second'], 21)
    ])      
    def test_score_abbreviation(self, abbr, pos_types, expected_result):
        
        char_values = word_abbreviator.load_char_values()
        
        actual_result = word_abbreviator.score_abbreviation(abbr, pos_types, char_values)
        self.assertEqual(actual_result, expected_result)   
       
    @parameterized.expand([
        ([('COL', 22), ('AND', 32), ('NOV', 312), ('LOV', 22), ('COL', 55), ('PAL', 32)], ['COL', 'LOV'])
    ])  
    def test_find_min_score_abbreviations(self, scored_abbr_list, expected_result):
        
        actual_result = word_abbreviator.find_min_scoring_abbreviations(scored_abbr_list)
        self.assertEqual(actual_result, expected_result)       

if __name__ == '__main__':
    unittest.main()