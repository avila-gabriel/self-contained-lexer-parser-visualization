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
FCALL -> 'id' '(' PARLISTCALL ')' 
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
