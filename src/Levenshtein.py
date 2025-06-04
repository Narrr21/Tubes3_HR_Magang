class Levenshtein:
    def __init__(self):
        self.pattern

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
            s1 : str = text[i:i+len(pattern)]
            if (self.are_strings_similar(s1, pattern, threshold)):
                result.append(i)
        return result
    
    def count_occurrence(self, text: str, pattern:str, threshold: float = 0.9):
        return len(self.search_positions(text, pattern, threshold))
    
    @staticmethod
    def search_multi_pattern(text: str, patterns: list[str]) -> dict[str, int]:
        results : dict[str, int] = {}
        if not text or not patterns: return results

        for pattern in patterns:
            lv : object = Levenshtein(pattern)
            num_occurrences = lv.count_occurrence(text)
            results[pattern] = num_occurrences
        return results

import unittest

if __name__ == "__main__":
    l = Levenshtein()
    print(l.calculate_distance("kitten", "Kitten"))