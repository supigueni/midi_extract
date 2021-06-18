"""
Created on 10.02.2019

@author: Gueni

converts midi files to a file with a c-array
this can be used to integrate in a embedded system to feed e.g. a motor with an sine generator

requirements to midi file:
- only one channel supported
- only one note at a time
"""

import mido
import sys, datetime, os

''' your input '''
file_path = 'HellsBells_XtraShort.mid'


# Useful constants from lazy_midi
MIDI_A4 = 69  # MIDI Pitch number
FREQ_A4 = 440.  # Hz
SEMITONE_RATIO = 2. ** (1. / 12.)  # Ascending


# from lazy_midi
def midi2freq(midi_number):
    """
    Given a MIDI pitch number, returns its frequency in Hz.
    """
    return FREQ_A4 * 2 ** ((midi_number - MIDI_A4) * (1. / 12.))


Errors = 0;
t_abs = 0;
ToneOn = 0;
NumNotes = 0;
buffer = []
freq = str(float(0.0)) + 'F,\t'
vel = str(float(0.0)) + 'F,\t'

mid = mido.MidiFile(file_path)
print(mid)

for msg in mid:
    print(msg)
    if (msg.type == 'note_on') | (msg.type == 'note_off'):
        t_abs = t_abs + msg.time
        NumNotes = NumNotes + 1
        time = str(float(round(max(msg.time, 0.001), 3))) + 'F'
        buffer.append('{' + freq + vel + time + '}')
        # update freq and vel delayed because of right alignment of time (midi is different than my c-function)
        freq = str(float(round(midi2freq(msg.note), 2))) + 'F,\t'
        vel = str(float(msg.velocity)) + 'F,\t'
        if ToneOn == 1:
            if msg.velocity == 0:
                ToneOn = 0
            else:
                print('Error: two notes at same time at', t_abs, 'seconds')
                Errors = Errors + 1
        if msg.velocity > 0:
            ToneOn = 1
if Errors > 0:
    print('Errors', Errors)
    sys.exit('program aborted')

print('absolute time', t_abs, 'seconds')

f = open("out.txt", "w")
f.write('/* created on ' + str(datetime.datetime.now()) + '    by ' + str(os.getlogin()) + '*/\n')
# f.write('/*' + str(mid) + '*/\n\n')
f.write('#define NUM_LENGTH    ' + str(NumNotes) + '\n\n')
NumParam = 3  # how much parameters are used
f.write('float32 MusicArray' + ']' + '[NUM_LENGTH][' + str(NumParam) + ']={\n')
f.write('/*freq,\t velocity,\t time*/\n')
i = 0
for x in buffer:
    if i < len(buffer) - 1:
        f.write(x + ',\n')
    else:
        f.write(x + '\n')
    i += 1
f.write('};')
f.close()
