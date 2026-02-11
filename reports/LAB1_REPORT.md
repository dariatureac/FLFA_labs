# Laboratory Work #1: Intro to Formal Languages & Finite Automata

**Course:** Formal Languages & Finite Automata  
**Author:** Daria Tureac  
**Variant:** 24

---

## Theory
A formal language is defined by a grammar $G = (V_n, V_t, P, S)$. In this laboratory work, we implement a Regular Grammar (Type 3 in the Chomsky hierarchy), where:
* $V_n = \{S, A, C, D\}$ — non-terminal symbols.
* $V_t = \{a, b\}$ — terminal symbols (alphabet).
* $S$ — the starting symbol.
* $P$ — production rules.

Because some states have multiple transitions for the same input symbol (e.g., $A \to bS$ and $A \to bD$), the resulting model is a Non-deterministic Finite Automaton (NFA).

---

## Objectives:
1. Understand the fundamental components of a formal language (alphabet, vocabulary, grammar).
2. Set up the project environment with a GitHub repository and Python.
3. Implement a `Grammar` class to represent the given variant and generate 5 valid strings.
4. Implement a `FiniteAutomaton` class to convert the grammar and validate input strings.

---

## Implementation description

* **Grammar Class**: This class stores the vocabulary and production rules. The `generate_string()` method uses a stochastic approach (via `random.choice`) to iteratively replace non-terminal symbols until only terminal characters remain.
* **FiniteAutomaton Class**: Unlike a simple DFA, this class handles non-determinism by maintaining a set of active states. For each input character, it calculates all possible next states. If, after processing the entire string, the set of active states contains the 'End' state, the string is accepted.
* **Transition Mapping**: Rules like $D \to bC$ are treated as transitions from $D$ to $C$ on input 'b', while rules like $C \to a$ lead directly to the final 'End' state.

---

## Code snippets
```python
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
```

## Conclusions/Screenshots/Results

**Console Output:**


Generated 5 valid strings
1. ababababaaba
2. ababbbbbbbbbabbbaaba
3. abaaaaaaabbbababbbabababababba
4. ababba
5. abba

**Interactive Validation**

Enter a string to check (or type 'exit' to quit): ababa
Is 'ababa' valid? True

Enter a string to check (or type 'exit' to quit): efheikgfhe
Is 'efheikgfhe' valid? False

**Conclusions**

 The project demonstrates the duality between Regular Grammars and Finite Automata. By implementing the transition logic, I observed that the provided grammar is non-deterministic, necessitating an NFA approach for string validation. The final implementation supports both automated generation of valid strings and manual user input validation, ensuring the robustness of the system.
## References
Course materials: "Formal Languages & Finite Automata" by Cretu Dumitru.

Python random module documentation.

Chomsky hierarchy of formal languages.