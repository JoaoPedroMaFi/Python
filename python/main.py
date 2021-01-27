# main.py

from Parser import Parser
from MusicPlay import MusicPlay

# faz a leitura do ficheiro
with open("./testes/exemplo4.in", mode="r") as fh:
    contents = fh.read()
# cria uma instancia da classe parser
parser = Parser()
# reconhece a parte lexica e gramatical
parser.Parse(contents)
# cria uma instancia da classe musicplay
save = MusicPlay()
# cria o ficheiro midi
save.writeSong(parser)
