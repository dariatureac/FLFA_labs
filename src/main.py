import random

class Grammar:
    def __init__(self):
        self.Vn = {'S', 'A', 'C', 'D'}
        self.Vt = {'a', 'b', 'd'}
        self.P = {
            'S': ['aA'],
            'A': ['bS', 'dD'],
            'D': ['bC', 'aD'],
            'C': ['a', 'bA']
        }
        self.start_symbol = 'S'

    def generate_string(self):
        word = self.start_symbol
        while any(char in self.Vn for char in word):
            new_word = ""
            for char in word:
                if char in self.Vn:
                    replacement = random.choice(self.P[char])
                    new_word += replacement
                else:
                    new_word += char
            word = new_word
        return word

    def to_finite_automaton(self):
        return FiniteAutomaton(self.Vn, self.Vt, self.P, self.start_symbol)

class FiniteAutomaton:
    def __init__(self, states, alphabet, rules, start_state):
        self.Q = states | {'End'}
        self.Sigma = alphabet
        self.delta = rules
        self.q0 = start_state
        self.F = {'End'}

    def check_string(self, input_string):
        current_state = self.q0
        for char in input_string:
            possible_moves = self.delta.get(current_state, [])
            next_state = None
            for move in possible_moves:
                if len(move) > 1 and move[0] == char:
                    next_state = move[1:]
                    break
                elif len(move) == 1 and move == char:
                    next_state = 'End'
                    break
            if next_state:
                current_state = next_state
            else:
                return False
        return current_state in self.F

if __name__ == "__main__":
    my_grammar = Grammar()
    print("--- Generated 5 valid strings ---")
    generated_list = [my_grammar.generate_string() for _ in range(5)]
    for i, s in enumerate(generated_list, 1):
        print(f"{i}. {s}")

    fa = my_grammar.to_finite_automaton()
    test_str = "abdba"
    print(f"\nIs '{test_str}' valid? {fa.check_string(test_str)}")