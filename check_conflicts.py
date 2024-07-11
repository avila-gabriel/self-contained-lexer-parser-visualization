import nltk
from nltk import CFG
from nltk.grammar import Nonterminal
from collections import defaultdict
import pprint

#ToDo arrumar isso, manualmente, de acordo com as regras dos slides. Seguir o que o professor fala no trabalho de como fzr isso.
#... tentar deixar LL1. Provavel q vai ter na tabela algum lugar q nao ha torna LL1 (2 opcoes em uma caixa). Aí será feito hardcode (espie o outro ToDo)
#... provavel que vai ter apenas 1 erro e é no if then else. Manda msg no grupo se precisar.

# É muito simples deixar o grammar num formato legivel pra essa api:
# A derivação tem que ser ->
# os não terminais precisam de single quotes (') ao redor
# tudo tem que ser separado por espaço
# por as derivações tudo na mesma linha separados por pipe (|)
# o epsilon é nada, então uma derivação que pode ir pra epsilon é só por o pipe (|) sem nada na esquerda
# não da pra usar a peninha (S'), então eu uso _prime no lugar mas pode ser qualquer coisa
# Example CFG with conflicts
grammar = CFG.fromstring("""
MAIN -> STMT | FLIST |
FLIST -> FDEF FLIST_tail
FLIST_tail -> FLIST |
FDEF -> 'def' 'id' '(' PARLIST ')' '{' STMTLIST '}'
PARLIST -> 'int' 'id' PARLIST_tail |
PARLIST_tail -> ',' PARLIST | 
STMT -> 'int' 'id' ';' | ATRIBST ';' | PRINTST ';' | RETURNST ';' | IFSTMT | '{' STMTLIST '}' | ';'
ATRIBST -> 'id' '=' ATRIBST_tail
ATRIBST_tail -> EXPR | FCALL
FCALL -> 'call' 'id' '(' PARLISTCALL ')' 
PARLISTCALL -> 'id' PARLISTCALL_tail
PARLISTCALL_tail -> ',' PARLISTCALL | 
PRINTST -> 'print' EXPR
RETURNST -> 'return' 
IFSTMT -> 'if' '(' EXPR ')' STMT IFSTMT_tail
IFSTMT_tail -> 'else' STMT |
STMTLIST -> STMT STMTLIST_tail
STMTLIST_tail -> STMTLIST |
EXPR -> NUMEXPR COMP_EXPR
COMP_EXPR -> '<' NUMEXPR | '>' NUMEXPR | '==' NUMEXPR |
NUMEXPR -> TERM NUMEXPR_prime
NUMEXPR_prime -> '+' TERM NUMEXPR_prime | '-' TERM NUMEXPR_prime |
TERM -> FACTOR TERM_prime
TERM_prime -> '*' FACTOR TERM_prime |
FACTOR -> 'num' | '(' NUMEXPR ')' | 'id'
""")


def compute_first_set(grammar):
    first = defaultdict(set)
    changes = True

    while changes:
        changes = False
        for production in grammar.productions():
            lhs = production.lhs()
            first_rhs = set()
            for symbol in production.rhs():
                # Check if symbol is a terminal by checking it's not an instance of Nonterminal
                if not isinstance(symbol, Nonterminal):
                    first_rhs = {symbol}
                    break
                first_rhs.update(first[symbol])
                if 'ε' not in first[symbol]:
                    break
            else:
                first_rhs.add('ε')
            
            if not first_rhs.issubset(first[lhs]):
                first[lhs].update(first_rhs)
                changes = True

    return first

def compute_follow_set(grammar, first):
    follow = defaultdict(set)
    start_symbol = grammar.start()
    follow[start_symbol].add('$')  # EOF symbol
    changes = True

    while changes:
        changes = False
        for production in grammar.productions():
            lhs = production.lhs()
            rhs = production.rhs()
            follow_rhs = follow[lhs]
            for i in range(len(rhs)-1, -1, -1):
                symbol = rhs[i]
                if not isinstance(symbol, Nonterminal):  # Terminal
                    follow_rhs = {symbol}
                else:  # Non-terminal
                    if 'ε' in first[symbol]:
                        follow[symbol].update(follow_rhs)
                    else:
                        follow[symbol] = follow_rhs.copy()
                    follow_rhs = first[symbol] - {'ε'}
                    if not follow_rhs:
                        follow_rhs = follow[symbol]

    return follow

def detect_conflicts(grammar, first, follow):
    conflicts = defaultdict(list)
    productions = list(grammar.productions())

    for i, prod_i in enumerate(productions):
        first_i = set()
        for symbol in prod_i.rhs():
            if not isinstance(symbol, Nonterminal):
                first_i = {symbol}
                break
            first_i.update(first[symbol])
            if 'ε' not in first[symbol]:
                break
        else:
            first_i.add('ε')

        for j, prod_j in enumerate(productions):
            if i == j or prod_i.lhs() != prod_j.lhs():
                continue

            first_j = set()
            for symbol in prod_j.rhs():
                if not isinstance(symbol, Nonterminal):
                    first_j = {symbol}
                    break
                first_j.update(first[symbol])
                if 'ε' not in first[symbol]:
                    break
            else:
                first_j.add('ε')

            if not first_i.isdisjoint(first_j):
                conflicts[prod_i.lhs()].append((prod_i, prod_j))

        if 'ε' in first_i:
            if not follow[prod_i.lhs()].isdisjoint(first_i):
                conflicts[prod_i.lhs()].append((prod_i, 'FOLLOW conflict with ' + str(follow[prod_i.lhs()])))

    return conflicts

first = compute_first_set(grammar)
follow = compute_follow_set(grammar, first)
conflicts = detect_conflicts(grammar, first, follow)

def print_pretty_sets_and_conflicts(first, follow, conflicts):
    pp = pprint.PrettyPrinter(indent=4)

    print("\nFIRST Sets:")
    for production in grammar.productions():
        lhs = production.lhs()
        if lhs in first:
            print(f"{lhs}: {first[lhs]}")

    print("\nFOLLOW Sets:")
    seen = set()
    for production in grammar.productions():
        lhs = production.lhs()
        if lhs not in seen:
            print(f"{lhs}: {follow[lhs]}")
            seen.add(lhs)

    print("\nConflicts:")
    for nonterminal, conflict_list in conflicts.items():
        print(f"\nConflicts in {nonterminal}:")
        for conflict in conflict_list:
            prod1, prod2 = conflict
            print(f"  Conflict between productions: {prod1} and {prod2}")

print_pretty_sets_and_conflicts(first, follow, conflicts)
