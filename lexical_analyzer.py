class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 0
        self.current_char = self.source_code[self.position]
        self.reserved_words = {
        'def': 'DEF',
        'int': 'INT',
        'return': 'RETURN',
        'if': 'IF',
        'else': 'ELSE',
        'print': 'PRINT',
        'call': 'CALL'
        }
        self.special_chars = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULT',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '{': 'LBRACK',
        '}': 'RBRACK',
        ',': 'COMMA',
        ';': 'SEMIC',
        '>': 'GT',
        '<': 'LT',
        '=': 'ASSIGN',
        '==': 'EQ'
        }

    def check_next_char(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        else:
            self.column += 1
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def recognize_token(self):
        tokens_value = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.check_next_char()
            elif self.current_char.isalpha():
                identifier = self.identifier()
                tokens_value.append(identifier)
            elif self.current_char.isdigit():
                number = self.number()
                tokens_value.append(number)
            elif self.current_char == '=':
                lexeme = self.equals()
                tokens_value.append(lexeme)
            elif self.current_char in self.special_chars.keys():
                if self.current_char != '(':
                    before = self.source_code[self.position - 1]
                    if before in ('=', '>', '<'):
                        self.error()
                tokens_value.append((self.special_chars[self.current_char], self.current_char))
                self.check_next_char()
            else:
                self.error()
        tokens = self.return_tokens(tokens_value)
        return tokens

    def identifier(self):
        result = ''
        before = self.source_code[self.position - 1]
        if before.isdigit(): #Para evitar declaração de varíavel começando com número
            self.error()
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.check_next_char()
        if result in self.reserved_words:
            return (self.reserved_words[result], result)
        else:
            return ('ID', result)

    def number(self):
        result = ''
        # before = self.source_code[self.position - 1]
        # if self.position < len(self.source_code):
        #     if before in self.special_chars:
        #         self.error()
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.check_next_char()
        return ('NUM', result)

    def equals(self):
        before = self.source_code[self.position - 1]
        if before in ('>', '<', '(', '{', '}', ',', ';', '+', '-', '*'):
            self.error()
        self.check_next_char()
        if self.current_char == '=' :
            self.check_next_char()
            return ('EQ', '==')
        else:
            return ('ASSIGN', '=')

    def return_tokens(self, tokens_value):
        final = []
        values = self.special_chars.values()
        for token in tokens_value:
            if token[0] in values:
                final.append(token[1])
            else:
                final.append(token[0].lower())
        final.append('$')
        return final

    def error(self):
        raise Exception(f'Invalid character \'{self.current_char}\' at line {self.line}, column {self.column}')

#Exemplo de uso
source_code = """
def func1(int A, int B) {
    if (A > B) {
        int C;
        C = 5;
    {
}
"""

#VERIFICAR CASOS DE ERRO LEXICO COMO 423423432A

lexer = Lexer(source_code)
try:
    tokens = lexer.recognize_token()
    print(tokens)
except Exception as e:
    print(e)
