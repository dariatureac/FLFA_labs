import random


class RegexInterpreter:
    def __init__(self, limit=5):
        self.limit = limit
'hiohioh'
    def generate(self, regex):
        result = ""
        i = 0
        while i < len(regex):
            char = regex[i]

            # 1. Handle Groups (Choice)
            if char == '(':
                end_group = regex.find(')', i)
                group_content = regex[i + 1:end_group]
                options = group_content.split('|')
                chosen = random.choice(options)

                # Check for quantifier after group, e.g., (X|Y|Z)^2
                i = end_group + 1
                multiplier = 1
                if i < len(regex) and regex[i] == '^':
                    i += 1
                    num_str = ""
                    while i < len(regex) and regex[i].isdigit():
                        num_str += regex[i]
                        i += 1
                    multiplier = int(num_str)

                result += chosen * multiplier
                continue

            # 2. Handle single characters with quantifiers
            else:
                current_char = char
                i += 1
                multiplier = 1

                if i < len(regex):
                    if regex[i] == '*':
                        multiplier = random.randint(0, self.limit)
                        i += 1
                    elif regex[i] == '+':
                        multiplier = random.randint(1, self.limit)
                        i += 1
                    elif regex[i] == '^':
                        i += 1
                        num_str = ""
                        while i < len(regex) and regex[i].isdigit():
                            num_str += regex[i]
                            i += 1
                        multiplier = int(num_str)

                result += current_char * multiplier
        return result

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


# --- Execution for Variant 4 ---
if __name__ == "__main__":
    interpreter = RegexInterpreter(limit=5)
    variant_4_regexes = [
        "(S|T)(U|V)W*Y+24",
        "L(M|N)O^3P*Q(2|3)",
        "R*S(T|U|V)W(X|Y|Z)^2"
    ]

    for regex in variant_4_regexes:
        # 1. Show processing sequence (Bonus Point)
        interpreter.show_step_by_step(regex)

        # 2. Generate valid strings
        print("Generated valid words:")
        samples = [interpreter.generate(regex) for _ in range(3)]
        print(f"  {{ {', '.join(samples)} }}")
