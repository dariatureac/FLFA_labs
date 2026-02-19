# Laboratory Work #2: Determinism in Finite Automata

**Course:** Formal Languages & Finite Automata  
**Author:** Daria Tureac  
**Variant:** 24

---

## Theory

The core of this laboratory is the study of Determinism versus Non-determinism.
* **NDFA (Non-deterministic Finite Automaton):** Allows multiple transitions for the same input symbol from a single state.
* **DFA (Deterministic Finite Automaton):** For every state and input symbol, there is exactly one transition.
* **Chomsky Hierarchy:** A classification system for formal grammars. Our variant belongs to Type 3 (Regular Grammars) because all rules follow the form $A \to aB$ or $A \to a$.

---

## Objectives:
1. Implement a method to classify the grammar based on the Chomsky hierarchy.

2. Convert the Finite Automaton (FA) back into a Regular Grammar.

3. Determine if the current FA is deterministic or non-deterministic.

4. Implement the conversion of an NDFA to a DFA to ensure predictable string validation.

---

## Implementation description

* **Chomsky Classification:** The `classify_grammar()` method analyzes the production rules. It verifies if the rules adhere to the format $A \to aB$ or $A \to a$ for Regular Grammars (Type 3) or if they satisfy the broader requirements of Context-Free (Type 2) or Context-Sensitive (Type 1) languages.
* **Determinism Check:** The `is_deterministic()` method iterates through the transition table. It specifically looks for states that map to multiple destination states for a single terminal symbol, identifying the non-determinism present in Variant 24 (where $A \to \{S, D\}$ on input 'b').
* **NDFA to DFA Conversion:** This is implemented using the Subset Construction Algorithm. The logic creates new "composite" states by grouping NFA states that can be reached simultaneously. These groups are represented as sorted tuples to maintain consistency and allow them to serve as dictionary keys.
* **FA to Grammar:** The `to_regular_grammar()` method reverses the automaton logic, turning state transitions back into production rules ($S \xrightarrow{a} A$ becomes $S \to aA$).

---

## Code snippets

**Classification Grammar**

I implemented the `classify_grammar` method to automatically determine the type of grammar based on its production rules.
```python
      def classify_grammar(self):
        # Chomsky Hierarchy Classification
        is_type_1 = True
        is_type_2 = True
        is_type_3 = True

        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                # Type 3 (Regular): A -> aB or A -> a
                if not ((len(rhs) == 1 and rhs in self.Vt) or
                        (len(rhs) == 2 and rhs[0] in self.Vt and rhs[1] in self.Vn)):
                    is_type_3 = False

                # Type 2 (Context-Free): LHS must be a single non-terminal
                if len(lhs) != 1 or lhs not in self.Vn:
                    is_type_2 = False

                # Type 1 (Context-Sensitive): |LHS| <= |RHS|
                if len(lhs) > len(rhs):
                    is_type_1 = False

        if is_type_3: return "Type 3 (Regular Grammar)"
        if is_type_2: return "Type 2 (Context-Free Grammar)"
        if is_type_1: return "Type 1 (Context-Sensitive Grammar)"
        return "Type 0 (Unrestricted Grammar)"

```
Logic: The function iterates through all rules. If a rule has more than one non-terminal on the right or symbols on the left (LHS), it is downgraded from Type 3.

**Determinism Check**

This function checks if the current Finite Automaton is a DFA or NDFA.
```python
        def is_deterministic(self):
        # Check for NDFA
        for state in self.Q:
            chars_seen = []
            if state in self.delta:
                for symbol, next_states in self.delta[state].items():
                    if len(next_states) > 1:  # Multiple transitions for same symbol
                        return False
        return True
```

Logic: Since my variant contains $A \to \{S, D\}$ for the input b, the function correctly identifies the automaton as Non-deterministic.

**NDFA to DFA**

I used the Subset Construction Algorithm to convert the NDFA into a DFA.
```python
        def is_deterministic(self):
        # Check for NDFA
        for state in self.Q:
            chars_seen = []
            if state in self.delta:
                for symbol, next_states in self.delta[state].items():
                    if len(next_states) > 1:  # Multiple transitions for same symbol
                        return False
        return True
```
Logic: The algorithm creates "composite states" (e.g., a state representing both $S$ and $D$). This removes ambiguity because for any input, the automaton now moves to exactly one composite state.

**FA to Grammar**

I implemented the `to_regular_grammar` method to transform the Finite Automaton back into a generative Grammar object.

```python
    def to_regular_grammar(self):
        # FA to Regular Grammar
        grammar_p = collections.defaultdict(list)
        for state, transitions in self.delta.items():
            for symbol, next_states in transitions.items():
                for ns in next_states:
                    if ns == 'End':
                        grammar_p[state].append(symbol)
                    else:
                        grammar_p[state].append(symbol + ns)
    return Grammar(self.Q, self.Sigma, dict(grammar_p), self.q0)
```
## Conclusions/Screenshots/Results

**Console Output:**


Grammar Type: Type 3 (Regular Grammar)

Is the original FA deterministic? False

NDFA to DFA Conversion Results:

New States (DFA): [('S',), ('A',), ('D', 'S'), ('C',), ('A', 'D'), ('End',), ('C', 'D', 'S'), ('D',), ('A', 'C'), ('A', 'D', 'End'), ('A', 'D', 'S')]
  
Transition from ('S',): {'a': ('A',)}
  
Transition from ('A',): {'b': ('D', 'S')}
  
Transition from ('D', 'S'): {'b': ('C',), 'a': ('A', 'D')}
  
Transition from ('C',): {'b': ('A',), 'a': ('End',)}
  
Transition from ('A', 'D'): {'b': ('C', 'D', 'S'), 'a': ('D',)}
  
Transition from ('End',): {}
  
Transition from ('C', 'D', 'S'): {'b': ('A', 'C'), 'a': ('A', 'D', 'End')}
  
Transition from ('D',): {'b': ('C',), 'a': ('D',)}
  
Transition from ('A', 'C'): {'b': ('A', 'D', 'S'), 'a': ('End',)}
  
Transition from ('A', 'D', 'End'): {'b': ('C', 'D', 'S'), 'a': ('D',)}
  
Transition from ('A', 'D', 'S'): {'b': ('C', 'D', 'S'), 'a': ('A', 'D')}

New Final States: [('End',), ('A', 'D', 'End')]

## Challenges & Difficulties

1. Immutability of Sets: In Python, sets cannot be used as dictionary keys. I solved this by converting sets of states into sorted tuples to represent the new composite states in the DFA.

2. State Explosion: Managing the mapping of all possible combinations of states (the power set) was complex, especially ensuring that transitions were correctly mapped from the original NDFA logic.

3. Final State Identification: Any composite state containing the original End state had to be marked as a final state in the new DFA.
## Conclusions

In conclusion, this laboratory work successfully demonstrated the transformation of a Non-deterministic Finite Automaton (NFA) into a Deterministic Finite Automaton (DFA) using the Subset Construction Algorithm. By implementing grammar classification and reverse conversion (FA to Grammar), I verified the theoretical link between Type-3 grammars and state machines within the Chomsky Hierarchy. Ultimately, the project highlights that while non-determinism allows for more concise designs, determinism is essential for building efficient, predictable recognition systems in computer science.

## References
Course materials: "Formal Languages & Finite Automata" by Cretu Dumitru.

Python random module documentation.

Chomsky hierarchy of formal languages.