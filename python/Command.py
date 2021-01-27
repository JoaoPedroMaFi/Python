# Command.py
import numpy as np


# comando para criar uma nota com valores numericos e depois transformaveis num ficheiro midi
def do_play(command, parser):
    # simbolo .
    if parser.music is None:  # se não existir nada, cria uma lista nova
        parser.music = [[parser.note, parser.time, 0]]
    else:  # se existir simplesmente adiciona outra lista a lista original
        note = parser.note
        time = parser.time
        parser.music.append([note, time, 0])
        if parser.flag == 1:  # flag usada para juntar tempos de notas
            note = parser.music[-2][0]
            time = parser.music[-2][1]
            time2 = parser.music[-1][1]
            time = time + time2
            if time > 128:
                time = 128
            parser.music[-2] = [note, time, 0]
            parser.music[-1] = None
            parser.music.remove(None)
            parser.flag = 0


# comando para subir valor da nota
def do_up(command, parser):
    # simbolo ^
    # note = parser.note
    # note = note + 1
    # parser.note = note
    parser.note += 1


# comando para descer valor da nota
def do_down(command, parser):
    # simbolo _
    note = parser.note
    note = note - 1
    parser.note = note


# comando para diminuir o tempo da nota
def do_slow(command, parser):
    # simbolo <
    if parser.time <= 64:
        time = parser.time
        time = int(time * 2)
        parser.time = time
    else:
        parser.time = 128


# comando para aumentar o tempo da nota
def do_fast(command, parser):
    # simbolo >
    if 2 <= parser.time <= 128:
        time = parser.time
        time = int(time // 2)  # faz divisao inteira
        parser.time = time
    else:
        parser.time = 1


# comando para criar uma pausa
def do_pause(commmand, parser):
    # simbolo *
    if parser.music is None:  # tempo da ultima nota
        parser.music = [[0, parser.time, 0]]
    else:
        parser.music.append([0, parser.time, 0])


# comando para juntar o tempo de duas notas, ativa a flag
def do_bound(commmand, parser):
    # simbolo ~
    parser.flag = 1


# comando para criar um acorde maior, ativa um flag que sera reconhecida no musicplay
def do_acm(commmand, parser):
    # simbolo :
    if parser.music is None:
        parser.music = [[parser.note, parser.time, 1]]

    else:
        note1 = parser.note
        time = parser.time
        parser.music.append([note1, time, 1])


# comando para subir valor da nota muito rapido
def do_megaup(commmand, parser):
    # simbolo ^{INT}
    if parser.music is None:
        parser.music = [[parser.note, parser.time, 0]]

    else:
        note = parser.note
        note = note + commmand.args['nota']
        if note > 127:
            note = 127
        parser.note = note


# comando para descer valor da nota muito rapido
def do_megadown(commmand, parser):
    # simbolo ^{INT}
    if parser.music is None:
        parser.music = [[parser.note, parser.time, 0]]

    else:
        note = parser.note
        note = note - commmand.args['nota']
        if note < 0:
            note = 1
        parser.note = note


# comando para criar uma macro e adiciona la numa symbol table
def do_macro(command, parser):
    list1 = command.args['commands']
    var = command.args['macroname']
    parser.vars[var] = list1


# comando para reproduzir a macro caso exista
def do_play_macro(command, parser):
    var = command.args['name']
    if var in parser.vars:
        parser.new_note = parser.note
        parser.new_time = parser.time
        list1 = parser.vars[var]
        command.exec(list1, parser)
        parser.note = parser.new_note
        parser.time = parser.new_time
    else:
        print("Macro not found")
        pass


# comando para procurar a letra com valor musical
def do_lettersearch(command, parser):
    # command [a-g]
    if parser.music is None:
        parser.music = []
        letter = parser.varsletters[command.args['letter']]
        note = find_nearest(letter, parser.note)
        parser.note = note
        parser.music.append([parser.note, parser.time, 0])

    else:
        letter = parser.varsletters[command.args['letter']]
        find_nearest(letter, parser.note)
        note = find_nearest(letter, parser.note)
        parser.note = note
        parser.music.append([parser.note, parser.time, 0])


# encontra a nota da letra em questao, com o valor mais proximo da ultima nota tocada
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


class Command:
    # dispatch table que reconhece os comandos devolvidos pelo parser
    dispatch_table = {"play": do_play,
                      "up": do_up,
                      "down": do_down,
                      "slow": do_slow,
                      "fast": do_fast,
                      "pause": do_pause,
                      "bound": do_bound,
                      "acm": do_acm,
                      "megaup": do_megaup,
                      "megadown": do_megadown,
                      "macro": do_macro,
                      "play_macro": do_play_macro,
                      "lettersearch": do_lettersearch}

    # definicao das variaveis iniciais da classe
    def __init__(self, command, args):
        self.name = command
        self.args = args

    # mostra os comandos recebidos
    def __repr__(self):
        return f"Command({self.name})"

    # funcao que procura na dispatch table que comando execuatr, conforme os parametros que receba
    def song(self, parser):
        self.dispatch_table[self.name](self, parser)

    @classmethod  # metodo de class que chama a funcao 'Song'
    def exec(cls, program, parser):
        print(program)
        for command in program:
            command.song(parser)
