# Boyer-Moore cuman pake 'Bad Character' heuristic karena Good Suffix gak di bahas di PPT 
class BM:
    # string pattern
    # int occurences
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.occ_table = self.init_lot()     # holds Last Occurence Values for all characters in text
        self.occurences = 0
    
    def set_pattern(self, pattern: str):
        self.pattern = pattern

    def get_num_occurrences(self) -> int:
        return self.occurences

    def init_lot(self) -> dict[str, int]:
        """
        Initializes Last Occurence Table
        """
        occ_table : dict[str, int] = {}
        idx: int = len(self.pattern)-1
        for i in range(idx, -1, -1):
            if self.pattern[i] not in occ_table:
                occ_table[self.pattern[i]] = i
        return occ_table

    def search_positions(self, text: str) -> list[int]:
        pat_len: int = len(self.pattern)
        text_len: int = len(text)

        if pat_len == 0: return []
        if pat_len > text_len: return []
        
        result: list[int] = []
        i_window_anchor: int = pat_len - 1

        while i_window_anchor < text_len:
            temp_i: int = i_window_anchor 

            i: int = i_window_anchor 
            j: int = pat_len - 1    

            while j >= 0 and text[i] == self.pattern[j]:
                i -= 1
                j -= 1
            
            if j < 0: 
                result.append(i + 1)
                i_window_anchor = temp_i + 1
            else: 
                mismatch: str = text[i]
                lx = self.occ_table.get(mismatch, -1)
                
                shift = j - lx
                i_window_anchor = temp_i + max(1, shift)
                
        return result

    def count_occurrence(self, text: str) -> int:
        result : list[int] = self.search_positions(text)
        self.occurences = len(result)
        return self.occurences

    @staticmethod
    def search_multi_pattern(text: str, patterns: list[str]) -> dict[str, int]:
        results: dict[str, int] = {}    # stores pattern, occurence
        if not text or not patterns: return {pattern: 0 for pattern in patterns}

        for pattern in patterns:
            bm: object = BM(pattern)
            num_occurrences = bm.count_occurrence(text)
            results[pattern] = num_occurrences if num_occurrences > 0 else 0

import unittest

class TestBM(unittest.TestCase):
    def test_simple_pattern_matching(self):
        """Test basic pattern matching functionality."""
        bm = BM("ab")
        count = bm.count_occurrence("ababab")
        self.assertEqual(count, 3)
        self.assertEqual(bm.get_num_occurrences(), 3)
        
    def test_no_matches(self):
        """Test when pattern is not found in text."""
        bm = BM("xyz")
        count = bm.count_occurrence("abcdefg")
        self.assertEqual(count, 0)
    
    def test_overlapping_patterns(self):
        """Test overlapping pattern matches."""
        bm = BM("aa")
        count = bm.count_occurrence("aaaa")
        self.assertEqual(count, 3)  # positions 0, 1, 2
        
        # Verify positions
        positions = bm.search_positions("aaaa")
        self.assertEqual(positions, [0, 1, 2])
    
    def test_single_character_pattern(self):
        """Test single character pattern."""
        bm = BM("a")
        count = bm.count_occurrence("banana")
        self.assertEqual(count, 3)
        
        positions = bm.search_positions("banana")
        self.assertEqual(positions, [1, 3, 5])
    
    def test_pattern_longer_than_text(self):
        """Test when pattern is longer than text."""
        bm = BM("longpattern")
        count = bm.count_occurrence("short")
        self.assertEqual(count, 0)
    
    def test_empty_inputs(self):
        """Test with empty text and pattern."""
        # Empty text
        bm = BM("test")
        count = bm.count_occurrence("")
        self.assertEqual(count, 0)
        
        # Empty pattern
        bm2 = BM("")
        count2 = bm2.count_occurrence("test")
        self.assertEqual(count2, 0)
        
        # Both empty
        bm3 = BM("")
        count3 = bm3.count_occurrence("")
        self.assertEqual(count3, 0)
    
    def test_identical_text_and_pattern(self):
        """Test when text and pattern are identical."""
        bm = BM("hello")
        count = bm.count_occurrence("hello")
        self.assertEqual(count, 1)
        
        positions = bm.search_positions("hello")
        self.assertEqual(positions, [0])
    
    def test_multiple_searches(self):
        """Test that multiple searches work correctly (counter resets)."""
        bm = BM("ab")
        
        # First search
        count1 = bm.count_occurrence("ababab")
        self.assertEqual(count1, 3)
        
        # Second search should reset counter
        count2 = bm.count_occurrence("abab")
        self.assertEqual(count2, 2)
        self.assertEqual(bm.get_num_occurrences(), 2)  # Should be from last search
    
    def test_case_sensitivity(self):
        """Test that pattern matching is case sensitive."""
        bm = BM("Hello")
        count = bm.count_occurrence("hello world Hello")
        self.assertEqual(count, 1)
        
        positions = bm.search_positions("hello world Hello")
        self.assertEqual(positions, [12])
    
    def test_special_characters(self):
        """Test with special characters and numbers."""
        bm = BM("a.b")
        count = bm.count_occurrence("a.b.a.b")
        self.assertEqual(count, 2)
        
        # Test with numbers
        bm2 = BM("123")
        count2 = bm2.count_occurrence("12312312345")
        self.assertEqual(count2, 3)
    
    def test_search_positions(self):
        """Test the search_positions method."""
        bm = BM("ana")
        positions = bm.search_positions("banana")
        self.assertEqual(positions, [1, 3])
        
        bm2 = BM("test")
        positions2 = bm2.search_positions("this is a test and another test")
        self.assertEqual(positions2, [10, 27])
    
    def test_long_text_performance(self):
        """Test with longer text to verify performance."""
        pattern = "needle"
        text = "hay" * 1000 + "needle" + "stack" * 1000 + "needle" + "more"
        
        bm = BM(pattern)
        count = bm.count_occurrence(text)
        self.assertEqual(count, 2)
        
        positions = bm.search_positions(text)
        self.assertEqual(len(positions), 2)
        for pos in positions:
            self.assertEqual(text[pos:pos+len(pattern)], pattern)
    def test_multi_pattern_count_occurrence(self):
        """Test searching multiple patterns in text."""
        text = "the quick brown fox jumps over the lazy dog"
        patterns = ["quick", "fox", "lazy", "cat"]
        
        results = BM.search_multi_pattern(text, patterns)
        
        expected_results = {
            "quick": 1,
            "fox": 1,
            "lazy": 1,
            "cat": 0
        }
        
        self.assertEqual(results, expected_results)

if __name__ == "__main__":
    unittest.main(verbosity=2)
    
    