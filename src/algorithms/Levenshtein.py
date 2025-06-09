class Levenshtein:
    def __init__(self):
        pass

    def calculate_distance(self, s1: str, s2: str) -> int:
        len_s1 : int = len(s1)
        len_s2 : int = len(s2)

        if len_s1 == 0: return len_s2
        if len_s2 == 0: return len_s1

        dp : list[list[int]] = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]  # contains distance for first i and j characters

        for i in range(len_s1 + 1):
            dp[i][0] = i
        
        for j in range(len_s2 + 1):
            dp[0][j] = j
        
        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost) 
        
        return dp[len_s1][len_s2]

    def calculate_similarity_percentage(self, s1: str, s2: str) -> float:
        if (len(s1) == 0 and len(s2) == 0) : return 1

        max_len : int = max(len(s1), len(s2))
        distance : int = self.calculate_distance(s1, s2)
        return 1 - (distance/max_len)

    def are_strings_similar(self, s1: str, s2: str, threshold: float) -> bool:
        return self.calculate_similarity_percentage(s1, s2) >= threshold
    
    def search_positions(self, text: str, pattern: str, threshold: float) -> list[int]:
        result : list[int] = []
        for i in range (0, len(text) - len(pattern) + 1):
            s1 : str = text[i:i+len(pattern)]                       # NOTE: both strings will always be the same size
            if (self.are_strings_similar(s1, pattern, threshold)):  # maybe instead of string winodw, process each words?
                result.append(i)
        return result
    
    def count_occurrence(self, text: str, pattern:str, threshold: float = 0.8):
        return len(self.search_positions(text, pattern, threshold))
    
    @staticmethod
    def search_multi_pattern(text: str, patterns: list[str]) -> dict[str, int]:
        results : dict[str, int] = {}
        if not text or not patterns: return results

        for pattern in patterns:
            lv : object = Levenshtein()
            num_occurrences = lv.count_occurrence(text, pattern)
            results[pattern] = num_occurrences
        return results

import unittest

class TestLevenshtein(unittest.TestCase):

    def setUp(self):
        self.lev = Levenshtein()

    def test_calculate_distance_basic_cases(self):
        self.assertEqual(self.lev.calculate_distance("kitten", "sitting"), 3)
        self.assertEqual(self.lev.calculate_distance("apple", "apply"), 1)
        self.assertEqual(self.lev.calculate_distance("test", "test"), 0)

    def test_calculate_distance_empty_strings(self):
        self.assertEqual(self.lev.calculate_distance("", ""), 0)
        self.assertEqual(self.lev.calculate_distance("abc", ""), 3)
        self.assertEqual(self.lev.calculate_distance("", "abc"), 3)

    def test_calculate_similarity_percentage(self):
        self.assertAlmostEqual(self.lev.calculate_similarity_percentage("kitten", "sitting"), 1.0 - (3/7.0))
        self.assertAlmostEqual(self.lev.calculate_similarity_percentage("test", "test"), 1.0)
        self.assertAlmostEqual(self.lev.calculate_similarity_percentage("test", ""), 0.0)
        self.assertEqual(self.lev.calculate_similarity_percentage("", ""), 1.0) # Based on your implementation

    def test_are_strings_similar(self):
        self.assertTrue(self.lev.are_strings_similar("apple", "apply", 0.75)) # Similarity is 0.8
        self.assertFalse(self.lev.are_strings_similar("apple", "apply", 0.85))
        self.assertTrue(self.lev.are_strings_similar("test", "test", 1.0))
        self.assertFalse(self.lev.are_strings_similar("kitten", "sitting", 0.70)) # Sim is ~0.57

    def test_search_positions(self):
        text = "the quick brown fox jumps over the lazy dog"
        pattern = "jump"
        self.assertEqual(self.lev.search_positions(text, "jumps", 1.0), [20])
        self.assertEqual(self.lev.search_positions(text, pattern, 0.75), [20])
        self.assertEqual(self.lev.search_positions(text, pattern, 0.90), [20])
        self.assertEqual(self.lev.search_positions("ababab", "aba", 1.0), [0, 2])

    def test_count_occurrence(self):
        text = "agcatagcatagcat"
        pattern = "agct"
        self.assertEqual(self.lev.count_occurrence(text, "agcat", 1.0), 3)
        self.assertEqual(self.lev.count_occurrence(text, pattern, 0.7), 3) 
        self.assertEqual(self.lev.count_occurrence(text, pattern, 0.8), 0)

    def test_search_multi_pattern_functionality(self):
        text = "the quick brown fox and the slow brown cat"
        patterns = ["brown", "fox", "foks", "cat", "dog", ""]
        
        expected_counts = {
            "brown": 2,
            "fox": 1,
            "foks": 0,
            "cat": 1,
            "dog": 0,
            "": len(text) + 1 
        }
        
        actual_counts = Levenshtein.search_multi_pattern(text, patterns)
        
        self.assertEqual(actual_counts, expected_counts)

    def test_search_multi_pattern_empty_inputs(self):
        self.assertEqual(Levenshtein.search_multi_pattern("", ["a", "b"]), {})
        self.assertEqual(Levenshtein.search_multi_pattern("some text", []), {})
        self.assertEqual(Levenshtein.search_multi_pattern("", []), {})

if __name__ == "__main__":
    unittest.main()