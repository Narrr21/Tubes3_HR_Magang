class KMP:
    def __init__(self, pattern:str = "test"):
        self.pattern = pattern
        self.num_occurrences = 0

    def compute_lps(self) -> list[int]:
        """
        Computes the longest prefix suffix (LPS) array for the pattern.
        """
        m = len(self.pattern)
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            if self.pattern[i] == self.pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    def count_occurence(self, text) -> int:
        """
        Searches for occurrences of the pattern in the given text using the KMP.
        Returns the number of occurrences found.
        """
        if not self.pattern or not text:
            return 0
            
        lps = self.compute_lps()
        n = len(text)
        m = len(self.pattern)
        i = 0  # index text
        j = 0  # index pattern
        
        self.num_occurrences = 0  # Reset
        
        while i < n:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m: # Found
                self.num_occurrences += 1
                j = lps[j - 1]
            elif i < n and self.pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return self.num_occurrences
                    
    def get_num_occurrences(self) -> int:
        """
        Returns the number of occurrences of the pattern found in the last search.
        """
        return self.num_occurrences

    def search_position(self, text) -> list[int]:
        """
        Finds all starting positions where the pattern occurs in the text.
        Returns a list of indices.
        """
        if not self.pattern or not text:
            return []
            
        positions = []
        lps = self.compute_lps()
        n = len(text)
        m = len(self.pattern)
        i = 0  # index text
        j = 0  # index pattern
        
        while i < n:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m: # Found
                positions.append(i - j)
                j = lps[j - 1]
            elif i < n and self.pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return positions
    
    def search_multi_pattern(self, text, patterns:list[str]) -> dict[str, int]:
        """
        Searches for multiple patterns in the text and returns a dictionary with pattern counts.
        """
        results = {}
        for pattern in patterns:
            kmp = KMP(pattern)
            count = kmp.count_occurence(text)
            results[pattern] = count
        return results

import unittest

class TestKMP(unittest.TestCase):
    def test_lps_computation(self):
        """Test LPS array computation for various patterns."""
        # Test case 1: Pattern with partial matches
        kmp = KMP("ABABCABAB")
        lps = kmp.compute_lps()
        expected = [0, 0, 1, 2, 0, 1, 2, 3, 4]
        self.assertEqual(lps, expected)
        
        # Test case 2: Repeating pattern
        kmp2 = KMP("AAAA")
        lps2 = kmp2.compute_lps()
        expected2 = [0, 1, 2, 3]
        self.assertEqual(lps2, expected2)
        
        # Test case 3: No repeating characters
        kmp3 = KMP("ABCDEF")
        lps3 = kmp3.compute_lps()
        expected3 = [0, 0, 0, 0, 0, 0]
        self.assertEqual(lps3, expected3)
    
    def test_simple_pattern_matching(self):
        """Test basic pattern matching functionality."""
        kmp = KMP("ab")
        count = kmp.count_occurence("ababab")
        self.assertEqual(count, 3)
        self.assertEqual(kmp.get_num_occurrences(), 3)
        
    def test_no_matches(self):
        """Test when pattern is not found in text."""
        kmp = KMP("xyz")
        count = kmp.count_occurence("abcdefg")
        self.assertEqual(count, 0)
    
    def test_overlapping_patterns(self):
        """Test overlapping pattern matches."""
        kmp = KMP("aa")
        count = kmp.count_occurence("aaaa")
        self.assertEqual(count, 3)  # positions 0, 1, 2
        
        # Verify positions
        positions = kmp.search_position("aaaa")
        self.assertEqual(positions, [0, 1, 2])
    
    def test_single_character_pattern(self):
        """Test single character pattern."""
        kmp = KMP("a")
        count = kmp.count_occurence("banana")
        self.assertEqual(count, 3)
        
        positions = kmp.search_position("banana")
        self.assertEqual(positions, [1, 3, 5])
    
    def test_pattern_longer_than_text(self):
        """Test when pattern is longer than text."""
        kmp = KMP("longpattern")
        count = kmp.count_occurence("short")
        self.assertEqual(count, 0)
    
    def test_empty_inputs(self):
        """Test with empty text and pattern."""
        # Empty text
        kmp = KMP("test")
        count = kmp.count_occurence("")
        self.assertEqual(count, 0)
        
        # Empty pattern
        kmp2 = KMP("")
        count2 = kmp2.count_occurence("test")
        self.assertEqual(count2, 0)
        
        # Both empty
        kmp3 = KMP("")
        count3 = kmp3.count_occurence("")
        self.assertEqual(count3, 0)
    
    def test_identical_text_and_pattern(self):
        """Test when text and pattern are identical."""
        kmp = KMP("hello")
        count = kmp.count_occurence("hello")
        self.assertEqual(count, 1)
        
        positions = kmp.search_position("hello")
        self.assertEqual(positions, [0])
    
    def test_multiple_searches(self):
        """Test that multiple searches work correctly (counter resets)."""
        kmp = KMP("ab")
        
        # First search
        count1 = kmp.count_occurence("ababab")
        self.assertEqual(count1, 3)
        
        # Second search should reset counter
        count2 = kmp.count_occurence("abab")
        self.assertEqual(count2, 2)
        self.assertEqual(kmp.get_num_occurrences(), 2)  # Should be from last search
    
    def test_case_sensitivity(self):
        """Test that pattern matching is case sensitive."""
        kmp = KMP("Hello")
        count = kmp.count_occurence("hello world Hello")
        self.assertEqual(count, 1)
        
        positions = kmp.search_position("hello world Hello")
        self.assertEqual(positions, [12])
    
    def test_special_characters(self):
        """Test with special characters and numbers."""
        kmp = KMP("a.b")
        count = kmp.count_occurence("a.b.a.b")
        self.assertEqual(count, 2)
        
        # Test with numbers
        kmp2 = KMP("123")
        count2 = kmp2.count_occurence("12312312345")
        self.assertEqual(count2, 3)
    
    def test_search_position(self):
        """Test the search_position method."""
        kmp = KMP("ana")
        positions = kmp.search_position("banana")
        self.assertEqual(positions, [1, 3])
        
        kmp2 = KMP("test")
        positions2 = kmp2.search_position("this is a test and another test")
        self.assertEqual(positions2, [10, 27])
    
    def test_long_text_performance(self):
        """Test with longer text to verify performance."""
        pattern = "needle"
        text = "hay" * 1000 + "needle" + "stack" * 1000 + "needle" + "more"
        
        kmp = KMP(pattern)
        count = kmp.count_occurence(text)
        self.assertEqual(count, 2)
        
        positions = kmp.search_position(text)
        self.assertEqual(len(positions), 2)
        for pos in positions:
            self.assertEqual(text[pos:pos+len(pattern)], pattern)
    def test_multi_pattern_count_occurence(self):
        """Test searching multiple patterns in text."""
        text = "the quick brown fox jumps over the lazy dog"
        patterns = ["quick", "fox", "lazy", "cat"]
        
        kmp = KMP("")
        results = kmp.search_multi_pattern(text, patterns)
        
        expected_results = {
            "quick": 1,
            "fox": 1,
            "lazy": 1,
            "cat": 0
        }
        
        self.assertEqual(results, expected_results)

if __name__ == "__main__":
    unittest.main(verbosity=2)