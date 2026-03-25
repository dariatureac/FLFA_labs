# Laboratory Work #4: Regular Expressions & String Generation

**Course:** Formal Languages & Finite Automata  
**Author:** Daria Tureac  
**Variant:** 4

---

## Theory

Regular Expressions (Regex) are a standardized syntax for representing Regular Languages. In computer science, they serve as a declarative way to define patterns that a string must follow. A regex engine typically converts these patterns into a Nondeterministic Finite Automaton (NFA) to validate or generate strings.

This laboratory focuses on the generative aspect: given a formal grammar defined by a regex, the program must produce valid "words" belonging to that language.

---

## Objectives:
1. Understand the syntax and logic of regular expressions (quantifiers, groups, and alternatives).
2. Implement a dynamic interpreter that generates valid strings based on a given regex input.
3. Handle specific quantifiers: * (Kleene star), + (at least one), and ^n (exact repetition).

---

## Implementation description and Code Snippets

The core of the project is the RegexInterpreter class. Unlike a simple text generator, it scans the regex string and maintains a pointer to interpret the logic on the fly.





**Handling Groups and Choices**

When the interpreter encounters a `(` , it finds the matching `)` and splits the content by the `|` delimiter.
```python
        if char == '(':
    end_group = regex.find(')', i)
    group_content = regex[i+1:end_group]
    options = group_content.split('|')
    chosen = random.choice(options) # Pick one alternative
    i = end_group + 1

```
Logic: This simulates a branching state in a finite automaton where the machine can take one of several available transitions.

**Quantifier Processing (*, +, ^n)**

After a character or a group, the code "looks ahead" to see if a quantifier follows.
```python
      if regex[i] == '*':
    multiplier = random.randint(0, self.limit) # 0 to 5
elif regex[i] == '+':
    multiplier = random.randint(1, self.limit) # 1 to 5
elif regex[i] == '^':
    # Logic to extract the integer after '^'
    multiplier = int(num_str)
```

Logic: This implements the loops and specific repetition counts required by the variant.

## Bonus Point: Processing Sequence Function

The function `show_step_by_step()` provides a logical trace of how the regex engine "sees" the input before it generates the result. This is crucial for verifying the precedence of operators.
```python    
def show_step_by_step(self, regex):
        print(f"\n[TRACE] Sequence of Processing for: {regex}")
        i = 0
        step_count = 1

        while i < len(regex):
            char = regex[i]

            if char == '(':
                end = regex.find(')', i)
                content = regex[i + 1:end]
                i = end + 1

                quant = ""
                if i < len(regex) and regex[i] == '^':
                    i += 1
                    while i < len(regex) and regex[i].isdigit():
                        quant += regex[i]
                        i += 1

                msg = f"Step {step_count}: Identified GROUP [{content}]"
                msg += f" with EXACT REPETITION ^{quant}" if quant else " with CHOICE '|'"
                print(f"  > {msg}")
            else:
                symbol = char
                i += 1
                quant_info = "LITERAL (Static)"
                if i < len(regex):
                    if regex[i] == '*':
                        quant_info = "KLEENE STAR (Repeat 0-5)"
                        i += 1
                    elif regex[i] == '+':
                        quant_info = "PLUS QUANTIFIER (Repeat 1-5)"
                        i += 1
                    elif regex[i] == '^':
                        i += 1
                        num = ""
                        while i < len(regex) and regex[i].isdigit():
                            num += regex[i]
                            i += 1
                        quant_info = f"EXACT REPETITION ^{num}"

                print(f"  > Step {step_count}: Processed SYMBOL '{symbol}' as {quant_info}")

            step_count += 1
```
Example Trace for Variant 4:

Regex: R*S(T|U|V)W(X|Y|Z)^2

Step 1: Identifies R followed by * (Kleene Star).

Step 2: Processes static literal S.

Step 3: Detects a Choice Group (T|U|V). One path is selected.

Step 4: Processes static literal W.

Step 5: Detects a Group with an Exact Repetition ^2. The entire selection from the group will be duplicated.

## Conclusions/Screenshots/Results

The interpreter successfully processed the following expressions:

`(S|T)(U|V)W*Y+24`

Sample: `SVWWWYYYY24`, `TUY24`

`L(M|N)O^3P*Q(2|3)`

Sample: `LNOOOQ3`, `LMOOOPPQ2`

`R*S(T|U|V)W(X|Y|Z)^2`

Sample: `RSUWXX`, `RRRSVWY Y`


## Challenges & Difficulties

* **Group Multipliers:** Applying `^2` to a group like `(X|Y|Z)^2` was challenging. The interpreter must first resolve the choice (e.g., pick `X`) and then apply the multiplier to the chosen character, resulting in `XX`.

* **Pointer Management:** Ensuring the index `i` skips exactly the right amount of characters after a group or a multi-digit power (like `^10`) required careful incrementation logic.
## Conclusions

This laboratory work demonstrates the bridge between formal grammar and string production. By building a dynamic interpreter, I proved that regular expressions can serve as a robust blueprint for data generation. The inclusion of the trace function highlights the deterministic nature of the parsing process, even when the output generation involves non-deterministic choices.
## References
[1] https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html

[2] https://en.wikipedia.org/wiki/Lexical_analysis

Course materials: Formal Languages & Finite Automata – Cretu Dumitru