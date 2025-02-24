# Midi to Desmos

## Overview

A program that converts data from MIDI files into a CSV format, allowing for import into Desmos and playback utilizing Desmos' tone() function. 

* Parses MIDI files to extract musical information - pitches, timings, tempo, etc.
* Converts into into a CSV format that can be copy pasted directly into Desmos
* Outputs `.txt` file containing MIDI data in human-readable format

## Desmos Integration

A corresponding Desmos project has been created with the necessary functions to represent the output table within Desmos. A sample song is already present in the project. 
[View Desmos project](https://www.desmos.com/calculator/747omxc8jw)

## Requirements

This project requires the `mido` Python library to parse MIDI files. Install the dependency (noted in `requirements.txt`) using pip. 

```
pip install -r requirements.txt
```

## Instructions

1. Place all MIDI files you want to convert in the `midi-files` folder. 
    ``` vbnet
    desmos-midi/
    └── midi_files/
        ├── song1.mid
        └── song2.mid
    ```

2. Open terminal in the repository's root directory and run `midi_to_csv.py`.

3. Follow the instructions in the terminal. When prompted for the name of the input file, provide only the file name, excluding the file extension.

4. All output files will be saved in the `output` folder. A CSV file will contain musical information in a Desmos-friendly format, and a `.txt` file contains MIDI data in a human-readable format.

5. Importing into Desmos:
    1. Open the CSV file in a plain text editor and copy all text in the file. 
    2. Visit the Desmos project created for this tool: [View Desmos project](https://www.desmos.com/calculator/747omxc8jw)
    3. Delete the pre-existing table. 
    4. Paste the text from the generated CSV file into Desmos. 

6. Set the slider for the *t* variable to 0 and press play on the ticker function. 

## Motivation

- Learning how MIDI files are structured, how data is stored, and how to extract data
- Practicing with Desmos functions (esp. piecewise)
- Practicing with Desmos actions

