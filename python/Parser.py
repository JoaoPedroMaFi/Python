# Parser.py

from Lexer import Lexer
import ply.yacc as yacc
import sys
from Command import Command


class Parser:
    tokens = Lexer.tokens # usa os tokens defenidos na classe LEXER

    def __init__(self):
        self.parser = None  # para guardar uma instancia do tipo parser, que vai conter o yacc
        self.lexer = None   #para guardar uma instancia do tipo lexer, que vai conter o Lexer desenvolvido
        self.music = None  # ser a lista de comandos ( abstract sintax tree)
        self.note = 60  # argumentos a passar, do valor da frequencia inicial
        self.time = 16  # argumentos a passar, do valor do temp inicial
        self.flag = 0  # para unir notas
        self.new_note = 0  # para manter a nota durante a macro
        self.new_time = 0  # para manter o tempo durante a macro
        self.vars = {}  # symbol table
        self.varsletters = {"c": (12, 24, 36, 48, 60, 72, 84, 96, 108, 120),  # Symbol table para as letras padrao
                            "d": (2, 14, 26, 38, 50, 62, 74, 86, 98, 110, 122),
                            "e": (4, 16, 28, 40, 52, 64, 76, 88, 100, 112, 124),
                            "f": (5, 17, 29, 41, 54, 65, 77, 89, 101, 113, 125),
                            "g": (7, 19, 31, 43, 55, 67, 79, 91, 103, 115, 127),
                            "a": (9, 21, 33, 45, 57, 69, 81, 93, 105, 117),
                            "b": (11, 23, 35, 47, 59, 71, 83, 95, 107, 119)}

    def Parse(self, input, **kwargs):
        self.lexer = Lexer()
        self.lexer.Build(input, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)
        program = self.parser.parse(lexer=self.lexer.lexer)
        Command.exec(program, self)
        print(self.music)

    def p_error(self, p):
        print(f"Syntax error '{p.value[0]}'", file=sys.stderr)
        exit(1)

    # axioma
    def p_music(self, p):
        """ music : command """
        p[0] = [p[1]]

    # axioma
    def p_music1(self, p):
        """ music  :  music command """
        lst = p[1]
        lst.append(p[2])
        p[0] = lst
    # conjunto de comandos
    def p_command(self, p):
        """ command : DOT
                    | UP
                    | DOWN
                    | FAST
                    | SLOW
                    | BOUND
                    | ACM
                    | MEGAPUSH
                    | MACRO
                    | PLAYMACRO
                    | LETTERNOTE
                    | PAUSE """
        p[0] = p[1]
    # gramatica para reconhecer,tocar a nota
    def p_dot(self, p):
        """ DOT : '.' """
        p[0] = Command("play", {"none": None})
    # gramatica para reconhecer, subir a nota
    def p_up(self, p):
        """ UP : '^' """
        p[0] = Command("up", {"none": None})
    # gramatica para reconhecer, descer a nota
    def p_down(self, p):
        """ DOWN : '_' """
        p[0] = Command("down", {"none": None})
    # gramatica para reconhecer, diminuir o tempo da nota
    def p_fast(self, p):
        """ FAST : '>' """
        p[0] = Command("fast", {"none": None})

    # gramatica para reconhecer, aumentar o tempo da nota
    def p_slow(self, p):
        """ SLOW : '<' """
        p[0] = Command("slow", {"none": None})

    # gramatica para reconhecer, uma pausa
    def p_pause(self, p):
        """ PAUSE : '*' """
        p[0] = Command("pause", {"none": None})

    # gramatica para reconhecer, um acorde maior
    def p_acm(self, p):
        """ ACM : ':' """
        p[0] = Command("acm", {"none": None})

    # gramatica para reconhecer,juntar tempo de duas notas
    def p_bound(self, p):
        """ BOUND : '.' '~' '.' """
        p[0] = Command("bound", {"none": None})

    # gramatica para reconhecer, aumentar a nota muito rapido
    def p_megapush(self, p):
        """ MEGAPUSH : '^' '{' INT '}'
                   | '_' '{' INT '}'"""
        if p[1] == '^':
            p[0] = Command("megaup", {"nota": p[3]})
        else:
            p[0] = Command("megadown", {"nota": p[3]})

    # gramatica para reconhecer, criacao de uma macro
    def p_macros(self, p):
        """ MACRO : MACRONAME '=' '[' music ']'"""
        p[0] = Command("macro", {"macroname": p[1], "commands": p[4]})

    # gramatica para reconhecer, para reproduzir uma macro
    def p_play_macro(self, p):
        """ PLAYMACRO : BARRA MACRONAME """
        p[0] = Command("play_macro", {"name": p[2]})

    # gramatica para reconhecer letras com valores musicais
    def p_letternote(self, p):
        """ LETTERNOTE : LETRAS """
        p[0] = Command("lettersearch", {"letter": p[1]})
