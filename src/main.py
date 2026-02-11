import random

class Grammar:
    def __init__(self):
        self.Vn = {'S', 'A', 'C', 'D'}
        self.Vt = {'a', 'b'}
        self.P = {
            'S': ['aA'],
            'A': ['bS', 'bD'],
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
        self.delta = rules
        self.q0 = start_state
        self.F = {'End'}

    def check_string(self, input_string):
        current_states = {self.q0}

        for char in input_string:
            next_states = set()
            for state in current_states:
                possible_moves = self.delta.get(state, [])
                for move in possible_moves:
                    if len(move) > 1 and move[0] == char:
                        next_states.add(move[1:])
                    elif len(move) == 1 and move == char:
                        next_states.add('End')

            if not next_states:
                return False
            current_states = next_states

        return any(state in self.F for state in current_states)


if __name__ == "__main__":
    my_grammar = Grammar()
    print("Generated 5 valid strings")
    generated_list = [my_grammar.generate_string() for _ in range(5)]
    for i, s in enumerate(generated_list, 1):
        print(f"{i}. {s}")

    fa = my_grammar.to_finite_automaton()

    print("\nInteractive Validation")
    while True:
        user_input = input("Enter a string to check (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            break

        is_valid = fa.check_string(user_input)
        print(f"Is '{user_input}' valid? {is_valid}\n")