"""
Created on 10.02.2019

@author: Gueni

Copyright (c) Christian Binder

Use of this source code is governed by a MIT license that can be
found in the LICENSE file.

Description:
converts midi files to a file with a c-array
this can be used to integrate in a embedded system to feed e.g. a motor with an sine generator

requirements to midi file:
- only one channel supported
- only one note at a time
"""

import mido
import datetime
import logging

# change level to logging.DEBUG to log all midi messages
logging.basicConfig(filename='result.log', filemode='w', level=logging.INFO)

# from lazy_midi
def midi2freq(midi_number):
    """
    Given a MIDI pitch number, returns its frequency in Hz.
    Source from lazy_midi.
    """
    midi_a4 = 69  # MIDI Pitch number
    freq_a4 = 440.  # Hz
    return freq_a4 * 2 ** ((midi_number - midi_a4) * (1. / 12.))


def convert_mid_to_text(file_in_path, file_out_path):
    logging.info(f'convert {file_in_path}')
    Errors = 0;
    t_abs = 0;
    ToneOn = 0;
    NumNotes = 0;
    buffer = []
    freq = str(float(0.0)) + 'F,\t'
    vel = str(float(0.0)) + 'F,\t'

    mid = mido.MidiFile(file_in_path)
    logging.debug(mid)

    for msg in mid:
        logging.debug(msg)
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
                    logging.error(f'Error: two notes at same time at {t_abs} seconds')
                    Errors = Errors + 1
            if msg.velocity > 0:
                ToneOn = 1
    if Errors > 0:
        logging.error(f'Errors: {Errors}')
        logging.error(f'convertion of file {file_in_path} aborted')
    else:
        logging.info(f'absolute time {t_abs} seconds')

        f = open(file_out_path, "w")
        f.write('/* created on ' + str(datetime.datetime.now()) + '    by ' + str(os.getlogin()) + '*/\n')
        # f.write('/*' + str(mid) + '*/\n\n')
        f.write('#define NUM_LENGTH    ' + str(NumNotes) + '\n\n')
        NumParam = 3  # how much parameters are used
        f.write(f'float32 MusicArray[NUM_LENGTH][{NumParam}] = ' + '{\n')
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
        logging.info(f'{file_out_path} finished')


if __name__ == '__main__':
    import os

    midi_files = os.listdir('in/')

    for file_in in midi_files:
        path_in = f'in/{file_in}'

        file_out = file_in.replace('.mid', '.h')
        path_out = f'out/{file_out}'

        convert_mid_to_text(path_in, path_out)

    logging.info('Program finished')
