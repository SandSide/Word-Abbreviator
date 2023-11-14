import unittest
import word_abbreviator

class TestWordSplit(unittest.TestCase):

    def test_split_words_with_valid_strings(self):
        s = ['Hello World', 'I like pancakes']
        
        expected_result = [
            ['HELLO', 'WORLD'],
            ['I', 'LIKE', 'PANCAKES']
        ]
        
        actual_result = word_abbreviator.split_words(s)
        
        for i in range(0, len(s)):
            self.assertEqual(actual_result[i], expected_result[i])
            

if __name__ == '__main__':
    unittest.main()