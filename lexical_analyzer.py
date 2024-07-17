#Classe para instanciar analisador léxico

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code #Input código
        self.position = 0 #Guarda o index do input para saber em qual caracter está o AL
        self.line = 1 #Identifica linha do input
        self.column = 0 #Identifica coluna do input
        self.current_char = self.source_code[self.position] #Char atual percorrido
        self.reserved_words = { #Palavras reservadas
        'def': 'DEF',
        'int': 'INT',
        'return': 'RETURN',
        'if': 'IF',
        'else': 'ELSE',
        'print': 'PRINT',
        'call': 'CALL'
        }
        self.special_chars = { #Caracteres especiais
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

    #Percorre caracter por caracter e atualiza atributos de linha, coluna e caracter conforme necessário
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

    #Identificar tokens com base nos lexemas
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
                    if before in ('=', '>', '<', '+', '-', '*'): #Para evitar criação de operadores inexistentes
                        self.error()
                tokens_value.append((self.special_chars[self.current_char], self.current_char))
                self.check_next_char()
            else:
                self.error()
        tokens = self.return_tokens(tokens_value)
        return tokens

    #Método para classificar lexema como token de tipo identificador
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

    #Método para classificar lexema como token de tipo num
    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.check_next_char()
        return ('NUM', result)

    #Método para classificar lexema como token de tipo EQUAL ou ASSIGN
    def equals(self):
        before = self.source_code[self.position - 1]
        if before in ('>', '<', '(', '{', '}', ',', ';', '+', '-', '*'): #Evitar criação de operadores inexistentes
            self.error()
        self.check_next_char()
        if self.current_char == '=' :
            self.check_next_char()
            return ('EQ', '==')
        else:
            return ('ASSIGN', '=')

    #Método para retornar lista de tokens identificados do input no formato desejado
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

    #Método para lançar exceção caso erro léxico seja identificado
    def error(self):
        raise Exception(f'Invalid character \'{self.current_char}\' at line {self.line - 1}, column {self.column}')

#Exemplos de código com erros léxicos
error_code1 = """
def error1(int A, int B) {
    int 34C;
    C = 20;
    if (A + B > C) {
        C => B - C;
    {
    else {
        C = A + B
    }
    if (C !== A + B) {
        print 1
    {
    else {
        print 0
    }
}
"""

error_code2 = """
def error2(int X, int Y) {
    int Z;
    Z = 50;
    if (X + Y > Z) {
        Z = X $ Y;
    {
    else {
        Z = X + Y
    }
    if (Z != X + Y) {
        return Z;
    }
    else {
        return 0;
    }
}
"""

error_code3 = """
def function ( int A , int B ) {
    int C = A + B;
    int D = B * C;
    int E = C * D;
    return E;
}

def main () {
    int C;
    int D;
    int R;
    C = 4;
    D = 5;
    R = function(C, D);
    if (R & C) {
        print #0
    } else {
        print 1
    }
    return;
}
"""

teste = """
int $;
"""

lexer = Lexer(teste)
try:
    tokens = lexer.recognize_token()
    print(tokens)
except Exception as e:
    print(e)
