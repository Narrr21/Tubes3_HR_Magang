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