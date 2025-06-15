from collections import defaultdict

ALPHABET_SIZE : int = 128 # ascii chars
class AhoCorasick:
    def __init__(self, patterns: list[str]):
        self.patterns: list[str] = patterns
        
        #   bitmasks. Index: state, value's bits: which words end in state.
        self.out: list[int] = []

        # index: state,  value: state to transition to on mismatch.
        self.fail: list[int] = []
        
        #  State transitions: trie[state][char code] gives the next state.
        self.trie: list[list[int]] = []

        self.build_trie()
        self.compute_failure_links()

    def add_state(self) -> int:
        """Helper to add a new state to all tables."""
        self.trie.append([-1] * ALPHABET_SIZE)
        self.out.append(0)
        self.fail.append(-1)
        return len(self.trie) - 1

    def build_trie(self) -> None:
        """
        Builds the initial Trie from the list of patterns and sets the initial output values.
        """
        root : int = self.add_state() # add state 0
        
        for i, pattern in enumerate(self.patterns):
            current_state : int = root
            for char in pattern:
                char_code : int = ord(char)
                if self.trie[current_state][char_code] == -1:
                    new_state : int = self.add_state()
                    self.trie[current_state][char_code] = new_state
                current_state = self.trie[current_state][char_code]
            
            # Mark the end of the pattern with a bitmask
            self.out[current_state] |= (1 << i)
    
    def compute_failure_links(self):
        """
        Computes failure links for all states and consolidates outputs using BFS.
        """
        queue : list[int] = []
        for char_code in range(ALPHABET_SIZE):
            state : int = self.trie[0][char_code]
            if state != -1:
                self.fail[state] = 0
                queue.append(state)
            else:
                self.trie[0][char_code] = 0
        
        while queue:
            state : int = queue.pop(0)
            for char_code in range(ALPHABET_SIZE):
                next_state : int = self.trie[state][char_code]
                if next_state != -1:
                    queue.append(next_state)

                    # Find failure link for next state
                    failure : int = self.fail[state]
                    while self.trie[failure][char_code] == -1:
                        failure = self.fail[failure]
                    
                    self.fail[next_state] = self.trie[failure][char_code]
                    
                    # Consolidate outputs from the failure state
                    self.out[next_state] |= self.out[self.fail[next_state]]

    @staticmethod
    def search_multi_pattern(text: str, patterns: list[str]) -> dict[str, int]:
        if not text or not patterns:
            return {p: 0 for p in patterns}

        ac = AhoCorasick(patterns)

        results: dict[str, int] = defaultdict(int)

        current_state: int = 0
        for i, char in enumerate(text):
            char_code: int = ord(char)
            if char_code >= ALPHABET_SIZE:
                current_state = 0
                continue

            while ac.trie[current_state][char_code] == -1:
                current_state = ac.fail[current_state]
            
            current_state = ac.trie[current_state][char_code]

            if ac.out[current_state] > 0:
                for j in range(len(ac.patterns)):
                    if (ac.out[current_state] & (1 << j)):
                        word: str = ac.patterns[j]
                        results[word] += 1
        
        final_results = {p: results[p] for p in patterns}
        
        return final_results


import unittest
class TestAhoCorasick(unittest.TestCase):    
    def test_basic_search(self):
        """Tests basic functionality with some present and some absent patterns."""
        text = "this is a simple test"
        patterns = ["is", "test", "simple", "notfound"]
        expected = {"is": 2, "test": 1, "simple": 1, "notfound": 0}
        self.assertEqual(AhoCorasick.search_multi_pattern(text, patterns), expected)

    def test_overlapping_and_substring_patterns(self):
        """Tests correct counting for patterns that are substrings of other patterns."""
        text = "bchaae"
        patterns = ["a"]
        # Should find "abc", "bche", and "he" (as part of "bche")
        expected = {"a": 2}
        self.assertEqual(AhoCorasick.search_multi_pattern(text, patterns), expected)
        
        text2 = "ahishershe"
        patterns2 = ["he", "she", "his", "hers"]
        expected2 = {"he": 2, "she": 2, "his": 1, "hers": 1}
        self.assertEqual(AhoCorasick.search_multi_pattern(text2, patterns2), expected2)

    def test_multiple_occurrences(self):
        """Tests patterns that appear multiple times."""
        text = "abababa"
        patterns = ["aba", "ab", "b"]
        expected = {"aba": 3, "ab": 3, "b": 3}
        self.assertEqual(AhoCorasick.search_multi_pattern(text, patterns), expected)

    def test_case_sensitivity(self):
        """Tests that the search is case-sensitive."""
        text = "He is he."
        patterns = ["He", "he", "is", "IS"]
        expected = {"He": 1, "he": 1, "is": 1, "IS": 0}
        self.assertEqual(AhoCorasick.search_multi_pattern(text, patterns), expected)

    def test_empty_and_no_match_cases(self):
        """Tests behavior with empty inputs and cases with no matches."""
        # Test with empty text
        self.assertEqual(AhoCorasick.search_multi_pattern("", ["a", "b"]), {"a": 0, "b": 0})
        # Test with empty pattern list
        self.assertEqual(AhoCorasick.search_multi_pattern("some text", []), {})
        # Test with no matches found
        self.assertEqual(AhoCorasick.search_multi_pattern("xyz", ["a", "b"]), {"a": 0, "b": 0})
        # Test with both empty
        self.assertEqual(AhoCorasick.search_multi_pattern("", []), {})
        
    def test_special_characters(self):
        """Tests functionality with non-alphabetic ASCII characters."""
        text = "test-123, test-456."
        patterns = ["test-", "123", ",", "."]
        expected = {"test-": 2, "123": 1, ",": 1, ".": 1}
        self.assertEqual(AhoCorasick.search_multi_pattern(text, patterns), expected)

if __name__ == '__main__':
    unittest.main()