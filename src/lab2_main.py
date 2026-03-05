import collections

class Grammar:
    def __init__(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.start_symbol = s

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


class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.Q = states
        self.Sigma = alphabet
        self.delta = transitions
        self.q0 = start_state
        self.F = final_states

    def is_deterministic(self):
        for state in self.delta:
            for symbol in self.delta[state]:
                if len(self.delta[state][symbol]) > 1:
                    return False
        return True

    def to_regular_grammar(self):
        grammar_p = collections.defaultdict(list)

        for state in self.delta:
            for symbol in self.delta[state]:
                for next_state in self.delta[state][symbol]:

                    grammar_p[state].append(symbol + next_state)

                    if next_state in self.F:
                        grammar_p[state].append(symbol)

        return Grammar(self.Q, self.Sigma, dict(grammar_p), self.q0)

    def convert_to_dfa(self):

        start = frozenset([self.q0])
        queue = [start]
        visited = set()
        dfa_delta = {}

        while queue:

            current = queue.pop(0)

            if current in visited:
                continue

            visited.add(current)
            dfa_delta[current] = {}

            for symbol in self.Sigma:

                next_states = set()

                for state in current:
                    if state in self.delta and symbol in self.delta[state]:
                        next_states.update(self.delta[state][symbol])

                if next_states:
                    next_states = frozenset(next_states)
                    dfa_delta[current][symbol] = next_states

                    if next_states not in visited:
                        queue.append(next_states)

        dfa_final = [s for s in visited if any(q in self.F for q in s)]

        return visited, dfa_delta, dfa_final


# функция для красивого вывода состояний
def format_state(state):
    return "{" + ",".join(sorted(state)) + "}"


if __name__ == "__main__":

    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}

    transitions = {
        'q0': {'b': {'q0', 'q1'}, 'a': {'q0'}},
        'q1': {'b': {'q2'}, 'a': {'q1'}},
        'q2': {'a': {'q2'}}
    }

    fa = FiniteAutomaton(states, alphabet, transitions, 'q0', {'q2'})

    grammar = fa.to_regular_grammar()

    print("1. Grammar Classification:")
    print(grammar.classify_grammar())

    print("\n2. Is FA deterministic?")
    print(fa.is_deterministic())

    new_states, new_delta, new_final = fa.convert_to_dfa()

    print("\n3. NFA → DFA")

    print("\nStates:")
    for s in new_states:
        print(format_state(s))

    print("\nTransitions:")
    for state in new_delta:
        for symbol in new_delta[state]:
            print(f"δ({format_state(state)}, {symbol}) = {format_state(new_delta[state][symbol])}")

    print("\nFinal states:")
    for s in new_final:
        print(format_state(s))