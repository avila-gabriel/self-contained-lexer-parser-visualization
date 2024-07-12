from collections import OrderedDict


parsing_table = {
    'A': {'a': ['C'], 'b': ['B'], 'e': ['B'], 'g': ['B'], 'i': ['B'], 'l': ['B'], 'm': ['B'], 'n': ['B'], '$': ['λ']},
    'B': {'b': ['li'], 'e': ['e', 'G', 'f'], 'g': ['g', 'b', 'i'], 'i': ['i'], 'l': ['J', 'i'], 'm': ['K', 'i'], 'n': ['L']},
    'C': {'a': ['D', 'E']},
    'D': {'a': ['a', 'b', 'c', 'F', 'd', 'e', 'G', 'f']},
    'E': {'a': ['C'], '$': ['λ']},
    'F': {'d': ['λ'], 'g': ['g', 'b', 'H']},
    'G': {'b': ['B', 'S'], 'e': ['B', 'S'], 'g': ['B', 'S'], 'i': ['B', 'S'], 'l': ['B', 'S'], 'm': ['B', 'S'], 'n': ['B', 'S']},
    'H': {'d': ['λ'], 'h': ['h', 'F']},
    'I': {'b': ['b', 'j', 'M']},
    'J': {'l': ['l', 'N']},
    'K': {'m': ['m']},
    'L': {'n': ['n', 'c', 'N', 'd', 'B', 'R']},
    'M': {'b': ['N'], 'c': ['N'], 'k': ['O'], 'v': 'N'},
    'N': {'b': ['T', 'U'], 'c': ['T', 'U'], 'v': ['T', 'U']},
    'O': {'k': ['k', 'b', 'c', 'P', 'd']},
    'P': {'b': ['b', 'Q']},
    'Q': {'d': ['λ'], 'h': ['h', 'P']},
    'R': {'b': ['λ'], 'e': ['λ'], 'f': ['λ'], 'g': ['λ'], 'l': ['λ'], 'm': ['λ'], 'n': ['λ'], 'o': ['ELSE DANGLING'], '$': ['λ']},
    'S': {'B': ['G'], 'e': ['G'], 'f': ['λ'], 'g': ['G'], 'i': ['G'], 'l': ['G'], 'l': ['G'], 'n': ['G']},
    'T': {'b': ['V', 'W'], 'c': ['V', 'W',], 'v': ['V', 'W']},
    'U': {'d': ['λ'], 'i': ['λ'], 'p': ['p', 'T'], 'q': ['q', 'T'], 'r': ['r', 'T']},
    'V': {'b': ['V', 'W'], 'c': ['V', 'W'], 'v': ['V', 'W']},
    'W': {'d': ['λ'], 'i': ['λ'], 'p': ['λ'], 'q': ['λ'], 'r': ['λ'], 's': ['s', 'V', 'W'], 't': ['t', 'V', 'W']},
    'X': {'b': ['b'], 'c': ['c', 'T', 'd'], 'v': ['v']},
    'Y': {'e': ['λ'], 'i': ['λ'], 'p': ['λ'], 'q': ['λ'], 'r': ['λ'], 's': ['λ'], 't': ['λ'], 'u': ['u', 'X', 'Y']}
}

mapping = {
    'A': 'MAIN',
    'B': 'STMT',
    'C': 'FLIST',
    'D': 'FDEF',
    'E': 'FLIST\'',
    'F': 'PARLIST',
    'G': 'STMTLIST',
    'H': 'PARLIST\'',
    'I': 'ATRIBST',
    'J': 'PRINTST',
    'K': 'RETURNST',
    'L': 'IFSTMT',
    'M': 'ATRIBST\'',
    'N': 'EXPR',
    'O': 'FCALL',
    'P': 'PARLISTCALL',
    'Q': 'PARLISTCALL\'',
    'R': 'IFSTMT\'',
    'S': 'STMTLIST\'',
    'T': 'NUMEXPR',
    'U': 'COMP_EXPR',
    'V': 'TERM',
    'W': 'NUMEXPR\'',
    'X': 'FACTOR',
    'Y': 'TERM\'',
    'λ': 'ε',  # epsilon
    'a': 'def',
    'b': 'id',
    'c': '(',
    'd': ')',
    'e': '{',
    'f': '}',
    'g': 'int',
    'h': ',',
    'i': ';',
    'j': '=',
    'k': 'call',
    'l': 'print',
    'm': 'return',
    'n': 'if',
    'o': 'else',
    'p': '<',
    'q': '>',
    'r': '==',
    's': '+',
    't': '-',
    'u': '*',
    'v': 'num'
}

def map_to_original(cell):
    return "".join([mapping.get(char, char) for char in cell])

translated_parsing_table = OrderedDict()

for non_terminal, rules in parsing_table.items():
    translated_non_terminal = map_to_original(non_terminal)
    translated_parsing_table[translated_non_terminal] = OrderedDict()
    for terminal, production in rules.items():
        translated_terminal = map_to_original(terminal)
        translated_production = [map_to_original(symbol) for symbol in production]
        translated_parsing_table[translated_non_terminal][translated_terminal] = translated_production

import pprint
pprint.pprint(translated_parsing_table)

"""
        parsing_table = {
                'MAIN': {'$': ['ε'],
                        ';': ['STMT'],
                        'def': ['FLIST'],
                        'id': ['STMT'],
                        'if': ['STMT'],
                        'int': ['STMT'],
                        'print': ['STMT'],
                        'return': ['STMT'],
                        '{': ['STMT']},
                'STMT': {';': [';'],
                        'id': ['print', ';'],
                        'if': ['IFSTMT'],
                        'int': ['int', 'id', ';'],
                        'print': ['PRINTST', ';'],
                        'return': ['RETURNST', ';'],
                        '{': ['{', 'STMTLIST', '}']},
                'FLIST': {'def': ['FDEF', "FLIST'"]},
                'FDEF': {'def': ['def', 'id', '(', 'PARLIST', ')', '{', 'STMTLIST', '}']},
                "FLIST'": {'$': ['ε'], 'def': ['FLIST']},
                'PARLIST': {')': ['ε'], 'int': ['int', 'id', "PARLIST'"]},
                'STMTLIST': {';': ['STMT', "STMTLIST'"],
                        'id': ['STMT', "STMTLIST'"],
                        'if': ['STMT', "STMTLIST'"],
                        'int': ['STMT', "STMTLIST'"],
                        'print': ['STMT', "STMTLIST'"],
                        'return': ['STMT', "STMTLIST'"],
                        '{': ['STMT', "STMTLIST'"]},
                "PARLIST'": {')': ['ε'], ',': [',', 'PARLIST']},
                'ATRIBST': {'id': ['id', '=', "ATRIBST'"]},
                'PRINTST': {'print': ['print', 'EXPR']},
                'RETURNST': {'return': ['return']},
                'IFSTMT': {'if': ['if', '(', 'EXPR', ')', 'STMT', "IFSTMT'"]},
                "ATRIBST'": {'(': ['EXPR'],
                        'call': ['FCALL'],
                        'id': ['EXPR'],
                        'num': ['EXPR']},
                'EXPR': {'(': ['NUMEXPR', 'COMP_EXPR'],
                        'id': ['NUMEXPR', 'COMP_EXPR'],
                        'num': ['NUMEXPR', 'COMP_EXPR']},
                'FCALL': {'call': ['call', 'id', '(', 'PARLISTCALL', ')']},
                'PARLISTCALL': {'id': ['id', "PARLISTCALL'"]},
                "PARLISTCALL'": {')': ['ε'], ',': [',', 'PARLISTCALL']},
                "IFSTMT'": {'$': ['ε'],
                        'else': ['ELSE DANGLING'],    
                        'id': ['ε'],
                        'if': ['ε'],
                        'int': ['ε'],
                        'print': ['ε'],
                        'return': ['ε'],
                        '{': ['ε'],
                        '}': ['ε']},
                "STMTLIST'": {';': ['STMTLIST'],
                        'STMT': ['STMTLIST'],
                        'if': ['STMTLIST'],
                        'int': ['STMTLIST'],
                        'print': ['STMTLIST'],
                        '{': ['STMTLIST'],
                        '}': ['ε']},
                'NUMEXPR': {'(': ['TERM', "NUMEXPR'"],
                        'id': ['TERM', "NUMEXPR'"],
                        'num': ['TERM', "NUMEXPR'"]},
                'COMP_EXPR': {')': ['ε'],
                        ';': ['ε'],
                        '<': ['<', 'NUMEXPR'],
                        '==': ['==', 'NUMEXPR'],
                        '>': ['>', 'NUMEXPR']},
                'TERM': {'(': ['TERM', "NUMEXPR'"],
                        'id': ['TERM', "NUMEXPR'"],
                        'num': ['TERM', "NUMEXPR'"]},
                "NUMEXPR'": {')': ['ε'],
                        '+': ['+', 'TERM', "NUMEXPR'"],
                        '-': ['-', 'TERM', "NUMEXPR'"],
                        ';': ['ε'],
                        '<': ['ε'],
                        '==': ['ε'],
                        '>': ['ε']},
                'FACTOR': {'(': ['(', 'NUMEXPR', ')'], 'id': ['id'], 'num': ['num']}, 
                "TERM'": {'*': ['*', 'FACTOR', "TERM'"],
                        '+': ['ε'],
                        '-': ['ε'],
                        ';': ['ε'],
                        '<': ['ε'],
                        '==': ['ε'],
                        '>': ['ε'],
                        '{': ['ε']}}
        }
"""
