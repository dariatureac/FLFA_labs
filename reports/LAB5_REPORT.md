# Laboratory Work #5: Chomsky Normal Form

**Course:** Formal Languages & Finite Automata  
**Author:** Daria Tureac  
**Variant:** 24

---

## Theory

Chomsky Normal Form (CNF) is a standardized representation of Context-Free Grammars (CFG).
A grammar is said to be in Chomsky Normal Form if all production rules follow one of the following structures:

```A → BC```

```A → a```

where:

* A, B, C are non-terminal symbols
* a is a terminal symbol

The purpose of converting a grammar into CNF is to simplify the analysis of context-free languages and make them easier to process by algorithms such as the CYK parsing algorithm.

To transform a grammar into CNF, several normalization steps must be applied:

1. Eliminate ε-productions.
2. Eliminate unit productions (renaming rules).
3. Remove inaccessible symbols.
4. Remove non-productive symbols.
5. Convert the grammar into Chomsky Normal Form.

These steps ensure that the grammar generates the same language while satisfying the CNF restrictions.

---

## Objectives:
1. Understand the concept of Chomsky Normal Form.
2. Learn the process of normalizing context-free grammars.
3. Implement an algorithm that converts an input grammar into Chomsky Normal Form.
4. Verify that the resulting grammar satisfies CNF rules.
---

## Grammar Normalization Process

**Step 1: Eliminating ε-productions**

The grammar contains the rule:

```B → ε```

This rule allows the variable B to produce the empty string.
To remove ε-productions, new productions are created by eliminating B from other rules where it appears.

Example:

```S → dB```

After removing ε:

```S → d```

Updated grammar:

```S → dB | A | d```

```A → d | dS | aBdAB```

```B → a | dA | A```

```C → Aa```

**Step 2: Eliminating Unit Productions**

Unit productions are rules of the form:

```A → B```

Examples in the grammar:

```S → A```

```B → A```

These rules are replaced by copying the productions of the referenced symbol.

After eliminating unit productions:

```S → dB | d | dS | aBdAB```

```A → d | dS | aBdAB```

```B → a | dA | d | dS | aBdAB```

```C → Aa```

**Step 3: Removing Non-Productive Symbols**

A symbol is productive if it can eventually generate a string consisting only of terminal symbols.

In this grammar:

```S, A, B, C```

are all productive symbols because they can derive terminal strings.

Therefore, no symbols are removed at this step.

**Step 4: Removing Inaccessible Symbols**

A symbol is inaccessible if it cannot be reached from the start symbol S.

Analyzing the grammar:

```C → Aa```

Symbol ```C``` is never referenced by other rules starting from S.

Therefore ```C``` is removed.

Updated grammar:

```S → dB | d | dS | aBdAB```

```A → d | dS | aBdAB```

```B → a | dA | d | dS | aBdAB```

**Step 5: Converting to Chomsky Normal Form**

Chomsky Normal Form requires that production rules contain:

* two non-terminals, or
* one terminal

Rules with terminals in longer productions must be replaced by new variables.

Example:

```a → T1```

```d → T2```

Then the rule:

```A → aBdAB```

becomes:

```A → T1 B T2 A B```

Since this rule still contains more than two symbols, it must be decomposed using new intermediate variables:

```A → T1 X1```

```X1 → B X2```

```X2 → T2 X3```

```X3 → A B```

This ensures every production satisfies CNF restrictions.


## Implementation description and Code Snippets

The solution is implemented in Python using a class called ```Grammar```.
This class stores the grammar structure and applies transformation methods.

Key methods include:




**Removing ε-productions**

```python
           def remove_epsilon(self):
        nullable = set()

        changed = True
        while changed:
            changed = False
            for A in self.P:
                for prod in self.P[A]:
                    if prod == ('ε',) or all(x in nullable for x in prod):
                        if A not in nullable:
                            nullable.add(A)
                            changed = True

        newP = defaultdict(list)

        for A in self.P:
            for prod in self.P[A]:
                indexes = [i for i,x in enumerate(prod) if x in nullable]

                for mask in range(1<<len(indexes)):
                    new_prod = list(prod)

                    for i,bit in enumerate(indexes):
                        if mask & (1<<i):
                            new_prod[bit] = None

                    new_prod = tuple([x for x in new_prod if x])

                    if new_prod:
                        newP[A].append(new_prod)

        self.P = newP

```
This function detects nullable variables and generates new rules that remove ε-productions while preserving the language.

**Removing Unit Productions**

```python
          def remove_unit(self):
        unit = set()

        for A in self.V:
            unit.add((A,A))

        changed = True
        while changed:
            changed = False
            for A in self.P:
                for prod in self.P[A]:
                    if len(prod)==1 and prod[0] in self.V:
                        B = prod[0]
                        for (C,D) in list(unit):
                            if D == A and (C,B) not in unit:
                                unit.add((C,B))
                                changed = True

        newP = defaultdict(list)

        for A,B in unit:
            for prod in self.P[B]:
                if not (len(prod)==1 and prod[0] in self.V):
                    newP[A].append(prod)

        self.P = newP
```

This method replaces rules of the form:

```A → B```

with all productions of B.

**Removing Non-Productive**

```python    
    def remove_nonproductive(self):
        productive = set()

        changed = True
        while changed:
            changed = False
            for A in self.P:
                for prod in self.P[A]:
                    if all(x in self.T or x in productive for x in prod):
                        if A not in productive:
                            productive.add(A)
                            changed = True

        self.V = self.V.intersection(productive)

        newP = defaultdict(list)
        for A in self.P:
            if A in productive:
                for prod in self.P[A]:
                    if all(x in self.T or x in productive for x in prod):
                        newP[A].append(prod)

        self.P = newP

```
This method identifies variables that cannot produce terminal strings and removes them from the grammar.

**Removing Inaccessible Symbols**

```python    
        def remove_unreachable(self):
        reachable = {self.S}

        changed = True
        while changed:
            changed = False
            for A in list(reachable):
                for prod in self.P.get(A,[]):
                    for x in prod:
                        if x in self.V and x not in reachable:
                            reachable.add(x)
                            changed = True

        self.V = self.V.intersection(reachable)

        newP = defaultdict(list)
        for A in self.P:
            if A in reachable:
                newP[A] = self.P[A]

        self.P = newP

```
The algorithm starts from the start symbol and keeps only symbols reachable through productions.

**Conversion to CNF**

```python    
         def to_cnf(self):
        new_rules = {}
        counter = 1

        # Replace terminals in long rules
        for A in list(self.P):
            new_list = []
            for prod in self.P[A]:
                if len(prod) >= 2:
                    new_prod = []
                    for x in prod:
                        if x in self.T:
                            if x not in new_rules:
                                new_var = f"T{counter}"
                                counter += 1
                                new_rules[x] = new_var
                                self.P[new_var] = [(x,)]
                                self.V.add(new_var)
                            new_prod.append(new_rules[x])
                        else:
                            new_prod.append(x)
                    new_list.append(tuple(new_prod))
                else:
                    new_list.append(prod)

            self.P[A] = new_list

        # Break long productions
        for A in list(self.P):
            new_list = []
            for prod in self.P[A]:
                if len(prod) <= 2:
                    new_list.append(prod)
                else:
                    current = list(prod)
                    prev = A
                    while len(current) > 2:
                        new_var = f"X{counter}"
                        counter += 1
                        self.V.add(new_var)

                        self.P[prev].append((current[0], new_var))

                        prev = new_var
                        current = current[1:]

                    self.P[prev] = [tuple(current)]
            self.P[A] = new_list

```
This function:

1. Replaces terminals inside long productions with new variables.
2. Breaks productions longer than two symbols into binary rules using helper variables.

## Conclusions/Screenshots/Results

After applying all normalization steps, the grammar is transformed into Chomsky Normal Form.

Example output:

```python
S → T2 B
S → d
S → T2 S
S → T1 X1

A → d
A → T2 S
A → T1 X1

B → a
B → T2 A
B → d
B → T2 S
B → T1 X1

T1 → a
T2 → d

X1 → B X2
X2 → T2 X3
X3 → A B


```
All productions follow CNF rules:

```A → BC```

```A → a```


## Challenges & Difficulties

One of the main challenges was correctly handling long productions such as:

```A → aBdAB```

These productions must be split into multiple binary productions while preserving the original structure of the grammar.

Another difficulty involved managing new variables introduced during normalization, ensuring they do not conflict with existing non-terminals.

## Conclusions

This laboratory work demonstrates the process of transforming a context-free grammar into Chomsky Normal Form.

The normalization procedure simplifies grammar structures and allows them to be used in parsing algorithms such as CYK.

Through the implementation, it was shown that any context-free grammar can be systematically transformed into CNF while preserving the language it generates.
## References
[1] https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html

[2] https://en.wikipedia.org/wiki/Lexical_analysis

Course materials: Formal Languages & Finite Automata – Cretu Dumitru