# Boyer-Moore cuman pake 'Bad Character' heuristic karena Good Suffix gak di bahas di PPT 
from collections import defaultdict
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
        results: dict[str, int] = defaultdict(int)    # stores pattern, occurence
        if not text or not patterns: return {pattern: 0 for pattern in patterns}

        for pattern in patterns:
            bm: object = BM(pattern)
            num_occurrences = bm.count_occurrence(text)
            results[pattern] = num_occurrences if num_occurrences > 0 else 0
        return results