import re
class Levenshtein:
    def __init__(self):
        pass

    def calculate_distance(self, s1: str, s2: str) -> int:
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        len_s1 = len(s1)
        len_s2 = len(s2)
        previous_row = list(range(len_s1 + 1))

        for i in range(1, len_s2 + 1):
            current_row = [i]
            
            for j in range(1, len_s1 + 1):
                insertion_cost = current_row[j-1] + 1
                deletion_cost = previous_row[j] + 1
                
                substitution_cost = previous_row[j-1]
                if s1[j-1] != s2[i-1]:
                    substitution_cost += 1
                
                current_row.append(min(insertion_cost, deletion_cost, substitution_cost))
            previous_row = current_row
        return previous_row[len_s1]

    def calculate_similarity_percentage(self, s1: str, s2: str) -> float:
        if (len(s1) == 0 and len(s2) == 0) : return 1

        max_len : int = max(len(s1), len(s2))
        distance : int = self.calculate_distance(s1, s2)
        return 1 - (distance/max_len)

    def are_strings_similar(self, s1: str, s2: str, threshold: float) -> bool:
        return self.calculate_similarity_percentage(s1, s2) >= threshold
    
    def search_positions(self, text: str, pattern: str, threshold: float) -> list[int]:
        result: list[int] = []
        word_iterator = re.finditer(r'\b\w+\b', text)
        
        for match in word_iterator:
            word = match.group(0)
            if self.are_strings_similar(word, pattern, threshold):
                result.append(match.start())
                
        return result
    
    def count_occurrence(self, text: str, pattern:str, threshold: float = 0.8):
        return len(self.search_positions(text, pattern, threshold))
    
    @staticmethod
    def search_multi_pattern(text: str, patterns: list[str]) -> dict[str, int]:
        results : dict[str, int] = {}
        if not text or not patterns: return results

        lv : object = Levenshtein()
        for pattern in patterns:
            num_occurrences = lv.count_occurrence(text, pattern)
            results[pattern] = num_occurrences
        return results