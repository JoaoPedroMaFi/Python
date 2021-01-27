from mxm.midifile import MidiOutFile

# classe que ira transforma uma lista de listas de valores nu ficheiro midi
class MusicPlay:

    def __init__(self):
        self.out_file = open("./testeProf/Letters/teste6Macro.mid", "wb")
        self.midi = MidiOutFile(self.out_file)

    def writeSong(self, parser):
        self.midi.header(format=0, nTracks=1, division=32)
        self.midi.start_of_track()
        melody = parser.music
        for note, duration, flag in melody:
            if flag == 1:
                note0 = note
                note1 = note + 4
                note2 = note + 7
                self.midi.update_time(0)
                self.midi.note_on(channel=0, note=note0)
                self.midi.note_on(channel=0, note=note1)
                self.midi.note_on(channel=0, note=note2)
                self.midi.update_time(duration)
                self.midi.note_off(channel=0, note=note0)
                self.midi.note_off(channel=0, note=note1)
                self.midi.note_off(channel=0, note=note2)
            else:
                self.midi.update_time(0)
                self.midi.note_on(channel=0, note=note)
                self.midi.update_time(duration)
                self.midi.note_off(channel=0, note=note)
        self.midi.update_time(0)
        self.midi.end_of_track()
