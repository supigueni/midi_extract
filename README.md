# midi_extract

Converts midi files to a text file with the midi data in a c-array.
This can be used to integrate in an embedded system to feed e.g., a motor with a sine generator

requirements to midi files:
- only one channel supported
- only one note at a time

In case your base is a more complex midi file you need to adapt it in a DAW before using midi_extract. If your midi file does not match the requirement the according timestamps will show up in the log file.

My favorite DAW is [Reaper](https://www.reaper.fm/), but you might also find some freeware like [Audiacity](https://www.audacity.de/).

## Installation

Requires python 3.6+

Install the "mido" package (library for working with MIDI messages and ports).

    pip install mido

Download the repository from GitHub

    cd c:\your_path\to_load
    git clone https://github.com/supigueni/midi_extract

## Usage
Put your midi files in the "in" folder and execute "Midi_extract.py"

    python Midi_extract.py
Find the output files stored in "out" folder. For detailed information of your conversion see "result.log"

## 3rd party SW
|Name|License
|----|-------
|[python](https://www.python.org/)|[PSF License](https://docs.python.org/3/license.html)
|[mido](https://pypi.org/project/mido/)|[OSI approved :: MIT License](https://pypi.org/search/?c=License+%3A%3A+OSI+Approved+%3A%3A+MIT+License)