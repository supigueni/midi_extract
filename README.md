# midi_extract

converts midi files to a text file with the midi data in a c-array.
This can be used to integrate in an embedded system to feed e.g. a motor with an sine generator

requirements to midi files:
- only one channel supported
- only one note at a time

usage:
- put your midi files in the in\ folder
- execute Midi_extract.py
- files stored in out\
- see results log in result.log
