from collections import defaultdict
import itertools

class Grammar:
    def __init__(self, variables, terminals, productions, start):
        self.V = set(variables)
        self.T = set(terminals)
        self.P = defaultdict(list)
        for left, rights in productions.items():
            for r in rights:
                self.P[left].append(tuple(r))
        self.S = start

    def print_grammar(self, title="Grammar"):
        print(f"\n{title}")
        for left in self.P:
            rights = ["".join(r) for r in self.P[left]]
            print(f"{left} -> {' | '.join(rights)}")


    # 1. Remove epsilon productions

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


    # 2. Remove unit productions

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


    # 3. Remove non productive symbols

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


    # 4. Remove unreachable symbols

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


    # 5. Convert to CNF

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



# Example: Variant 24 grammar


variables = {"S","A","B","C"}
terminals = {"a","d"}

productions = {
"S":[("d","B"),("A",)],
"A":[("d",),("d","S"),("a","B","d","A","B")],
"B":[("a",),("d","A"),("A",),("ε",)],
"C":[("A","a")]
}

g = Grammar(variables,terminals,productions,"S")

g.print_grammar("Original Grammar")

g.remove_epsilon()
g.print_grammar("After removing ε-productions")

g.remove_unit()
g.print_grammar("After removing unit productions")

g.remove_nonproductive()
g.print_grammar("After removing nonproductive symbols")

g.remove_unreachable()
g.print_grammar("After removing unreachable symbols")

g.to_cnf()
g.print_grammar("Chomsky Normal Form")