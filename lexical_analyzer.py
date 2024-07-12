class Lexer:
    def __init__(self):
        pass

    def check_next_char(self):
        pass

    def recognize_token(self):
        pass

    def identifier(self):
        pass

    def number(self):
        pass

    def equals(self):
        pass

    def error(self):
        pass

source_code = ""
lexer = Lexer()

try:
    tokens = lexer.recognize_token()
    for token in tokens:
        print(token)
except Exception as e:
    print(e)
