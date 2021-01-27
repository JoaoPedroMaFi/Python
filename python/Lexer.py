# Lexer.py
import ply.lex as lex
import sys


class Lexer:
    literals = "\.<>:_{}*~^=[]" # a maior parte do lexer a desenvolver são literais, aqui apresentados
    tokens = ("NOTREAD", "INT", "MACRONAME", "BARRA", "LETRAS") # tokens necessarios para desenvolver corretamente o Lexer
    t_ignore = " \n\t"  # tokens a ignorar para este projeto

    def t_NOTREAD(self, t):
        r"""\#.*\n|\#.*""" # nao reconhecer expressoes comecados por '#'
        pass

    def t_INT(self, t):
        r"""[0-9]+""" # reconhece e devolve os valores numericos usados para subir rapidamente notas
        t.value = int(t.value)
        return t

    def t_MACRONAME(self, t): # reconhece o nome das macros que tem que começar por maiusculas
        r"""[A-Z]+([0-9a-zA-Z]+)?"""
        return t

    def t_BARRA(self, t): # reconhece a barra invertida, utilizada no chamamentos das macros
        r"""[\\]"""
        return t

    def t_LETRAS(self, t): # reconhece as letras que sao usadas normalmente em musica de vai de a ate g
        r"""[a-g]"""
        return t

    def t_error(self, t):
        print(f"Lexer error. Unexpected char: '{t.value[0]}'", file=sys.stderr)
        exit(1)

    def __init__(self):
        self.lexer = None # Construtor da classe Lexer

    def Build(self, input, **kwargs): # Método para inicializar o lexer e atribuir os valores do input
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.input(input)
