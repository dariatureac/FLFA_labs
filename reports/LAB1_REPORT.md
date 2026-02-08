# Laboratory Work #1: Intro to Formal Languages & Finite Automata

**Course:** Formal Languages & Finite Automata  
**Author:** Daria Tureac  
**Variant:** 24

---

## Theory
A formal language is a set of strings over an alphabet, defined by a grammar $G = (V_n, V_t, P, S)$. For regular grammars (Type 3 in the Chomsky hierarchy), the production rules are restricted to a specific format that allows them to be modeled by a Finite Automaton (FA). A Finite Automaton is a computational model that transitions through states based on input symbols to verify if a string belongs to the language.

---

## Objectives:
1. Understand the fundamental components of a formal language (alphabet, vocabulary, grammar).
2. Set up the project environment with a GitHub repository and Python.
3. Implement a `Grammar` class to represent the given variant and generate 5 valid strings.
4. Implement a `FiniteAutomaton` class to convert the grammar and validate input strings.

---

## Implementation description

* **Grammar Class**: This class stores the non-terminal symbols $\{S, A, C, D\}$, terminal symbols $\{a, b, d\}$, and the production rules. The `generate_string()` method starts with the symbol $S$ and iteratively replaces non-terminals using `random.choice` until only terminal characters remain in the string.
* **FiniteAutomaton Class**: This class represents the state machine. It maps grammar rules to a transition dictionary. For example, the rule $S \to aA$ is stored as a transition from state $S$ to $A$ on input 'a'. It includes a `check_string()` method that follows these transitions to accept or reject an input.
* **Conversion Logic**: The `to_finite_automaton()` method automatically maps terminal productions (like $C \to a$) to a special 'End' state, which serves as the final/accepting state for the automaton.

---

## Code snippets
```python
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
```

## Conclusions/Screenshots/Results

**Console Output:**


Generated 5 valid strings 
1. abadbbbababadaaaaaabbdbbbadabbbadaaba
2. ababababababababadba
3. ababadaba
4. abababadba
5. abadba

**Validation Tests**

Is 'abdba' valid? False

**Analysis:**

The implementation successfully generates strings according to the rules of Variant 24. The validation for abdba returned False, which is correct because the grammar rules do not allow a 'b' to immediately follow an 'a' when transitioning to state 'D'.

## References
Course materials: "Formal Languages & Finite Automata" by Cretu Dumitru.

Python random module documentation.

Chomsky hierarchy of formal languages.