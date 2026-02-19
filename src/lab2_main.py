import collections


class Grammar:
    def __init__(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.start_symbol = s

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


class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.Q = states
        self.Sigma = alphabet
        self.delta = transitions
        self.q0 = start_state
        self.F = final_states

    def is_deterministic(self):
        # Check for NDFA
        for state in self.Q:
            chars_seen = []
            if state in self.delta:
                for symbol, next_states in self.delta[state].items():
                    if len(next_states) > 1:  # Multiple transitions for same symbol
                        return False
        return True

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

    def convert_to_dfa(self):
        # NDFA to DFA Conversion (Subset Construction)
        dfa_q0 = tuple(sorted([self.q0]))
        dfa_delta = {}
        dfa_states = [dfa_q0]
        visited = []

        while dfa_states:
            current_composite_state = dfa_states.pop(0)
            if current_composite_state in visited: continue
            visited.append(current_composite_state)

            dfa_delta[current_composite_state] = {}

            for symbol in self.Sigma:
                next_set = set()
                for sub_state in current_composite_state:
                    if sub_state in self.delta and symbol in self.delta[sub_state]:
                        next_set.update(self.delta[sub_state][symbol])

                if next_set:
                    next_state_tuple = tuple(sorted(list(next_set)))
                    dfa_delta[current_composite_state][symbol] = next_state_tuple
                    if next_state_tuple not in visited:
                        dfa_states.append(next_state_tuple)

        # New final states are any sets containing an original final state
        dfa_f = [q for q in visited if any(s in self.F for s in q)]
        return visited, dfa_delta, dfa_f


# --- Main Execution ---
if __name__ == "__main__":
    vn = {'S', 'A', 'C', 'D'}
    vt = {'a', 'b'}
    rules = {
        'S': {'a': {'A'}},
        'A': {'b': {'S', 'D'}},
        'D': {'b': {'C'}, 'a': {'D'}},
        'C': {'a': {'End'}, 'b': {'A'}}
    }

    fa = FiniteAutomaton(vn, vt, rules, 'S', {'End'})

    #Classification
    grammar = fa.to_regular_grammar()
    print(f"1. Grammar Type: {grammar.classify_grammar()}")

    #Determinism Check
    print(f"2. Is the original FA deterministic? {fa.is_deterministic()}")

    #NDFA to DFA Conversion
    new_states, new_delta, new_final = fa.convert_to_dfa()
    print("\n3. NDFA to DFA Conversion Results:")
    print(f"New States (DFA): {new_states}")
    for state, trans in new_delta.items():
        print(f"  Transition from {state}: {trans}")
    print(f"New Final States: {new_final}")