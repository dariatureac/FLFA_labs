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

### Chomsky Classification

The `classify_grammar()` method analyzes the production rules of the grammar and determines its position in the Chomsky hierarchy.

A grammar is classified as **Type 3 (Regular)** if all rules follow the form:

A → aB  
A → a

If some rules violate this structure, the grammar may belong to a higher type (Type 2 or Type 1).

---

### Determinism Check

The `is_deterministic()` method checks whether the automaton is deterministic.

It scans the transition table and verifies if a state has **more than one possible transition for the same input symbol**.

In **Variant 24**, the automaton is non-deterministic because:

δ(q0, b) = {q0, q1}

Since two possible states exist for the same input, the automaton is classified as **NDFA**.

---

### NDFA to DFA Conversion

The NDFA is converted to a DFA using the **Subset Construction Algorithm**.

Instead of single states, the DFA uses **sets of NFA states**, for example:

{q0}  
{q0,q1}  
{q0,q1,q2}

Each set represents all states the NDFA could be in at that moment.  
Transitions are calculated by combining transitions from all states inside the set.

---

### FA to Grammar

The `to_regular_grammar()` method converts automaton transitions into grammar rules.

A transition

qi --a--> qj

is converted into the production rule:

qi → aqj

If the destination state is **final**, an additional rule is added:

qi → a

This allows the grammar to generate valid terminal strings.
---

## Code snippets

**Classification Grammar**

I implemented the `classify_grammar` method to automatically determine the type of grammar based on its production rules.
```python
          def classify_grammar(self):
        is_type3 = True
        is_type2 = True
        is_type1 = True

        for lhs, rhs_list in self.P.items():

            if lhs not in self.Vn:
                is_type2 = False

            for rhs in rhs_list:

                # Type 3: A -> a or A -> aB
                if len(rhs) == 1:
                    if rhs not in self.Vt:
                        is_type3 = False

                elif len(rhs) >= 2:
                    terminal = rhs[0]
                    nonterminal = rhs[1:]

                    if terminal not in self.Vt or nonterminal not in self.Vn:
                        is_type3 = False
                else:
                    is_type3 = False

                # Type 1 condition
                if len(lhs) > len(rhs):
                    is_type1 = False

        if is_type3:
            return "Type 3 (Regular Grammar)"
        elif is_type2:
            return "Type 2 (Context-Free Grammar)"
        elif is_type1:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"

```
Logic: The function iterates through all rules. If a rule has more than one non-terminal on the right or symbols on the left (LHS), it is downgraded from Type 3.

**Determinism Check**

This function checks if the current Finite Automaton is a DFA or NDFA.
```python
        def is_deterministic(Q, delta):
    for state in Q:
        if state in delta:
            for symbol, next_states in delta[state].items():
                if len(next_states) > 1:
                    return False
    return True
```

Logic: If any state has more than one transition for the same symbol, the automaton is classified as NDFA.
**NDFA to DFA**

I used the Subset Construction Algorithm to convert the NDFA into a DFA.
```python
        def nfa_to_dfa(Q, Sigma, delta, q0, F):
    start_state = tuple(sorted([q0]))
    dfa_states = [start_state]
    dfa_transitions = {}
    dfa_final_states = []

    i = 0
    while i < len(dfa_states):
        current = dfa_states[i]
        dfa_transitions[current] = {}

        for symbol in Sigma:
            next_state = set()

            for s in current:
                if s in delta and symbol in delta[s]:
                    next_state.update(delta[s][symbol])

            next_state = tuple(sorted(next_state))
            dfa_transitions[current][symbol] = next_state

            if next_state not in dfa_states:
                dfa_states.append(next_state)

        i += 1

    for state in dfa_states:
        if any(s in F for s in state):
            dfa_final_states.append(state)

    return dfa_states, dfa_transitions, dfa_final_states
```
Logic: The algorithm creates composite states representing groups of NDFA states.

Example:

{q0} – start state

{q0,q1} – reachable from q0 with input b

{q0,q1,q2} – reachable from {q0,q1} with input b

These new grouped states ensure that the resulting automaton behaves deterministically.
**FA to Grammar**

I implemented the `to_regular_grammar` method to transform the Finite Automaton back into a generative Grammar object.

```python
        def to_regular_grammar(self):
        grammar_p = collections.defaultdict(list)

        for state in self.delta:
            for symbol in self.delta[state]:
                for next_state in self.delta[state][symbol]:

                    grammar_p[state].append(symbol + next_state)

                    if next_state in self.F:
                        grammar_p[state].append(symbol)

        return Grammar(self.Q, self.Sigma, dict(grammar_p), self.q0)
```
## Conclusions/Screenshots/Results

**Console Output:**


1. Grammar Classification:
Type 3 (Regular Grammar)

2. Is FA deterministic?
False

3. NFA → DFA

States:
{q0,q1,q2}
{q0}
{q0,q1}

Transitions:
δ({q0}, a) = {q0}
δ({q0}, b) = {q0,q1}
δ({q0,q1}, a) = {q0,q1}
δ({q0,q1}, b) = {q0,q1,q2}
δ({q0,q1,q2}, a) = {q0,q1,q2}
δ({q0,q1,q2}, b) = {q0,q1,q2}

Final states:
{q0,q1,q2}

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