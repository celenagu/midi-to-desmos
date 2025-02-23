import csv
from mido import MidiFile

# Convert midi note to frequency
def midi_to_freq(n):
    return 440.0*2**((n-69) / 21.0)

def ticks_to_time(ticks, tpb, tempo):
    us_per_tick = tempo / tpb
    return int(ticks * us_per_tick / 1000) 


def midi_to_csv(file_name):
    in_file = "midi_files/" + file_name + ".mid"
    out_file = file_name + ".csv"
    
    print(f"Reading midi file {in_file}")
    
    # load in midi file
    midi = MidiFile(in_file)
    events = []
    
    # Display general MIDI info
    print(f"Number of tracks: {len(midi.tracks)}")
    tpb = midi.ticks_per_beat
    print(f"Ticks per beat: {tpb}")
    
    # Get initial tempo (default 120 BPM, 500000 us/beat)
    tempo = 500000
    
    # Track currently active notes
    active_notes = {}

    # Process each track and event
    for i, track in enumerate(midi.tracks):
        print(f"\nProcessing Track {i}: {track.name}")
        abs_time = 0
        
        for msg in track:
            print(msg)
            abs_time += msg.time
            ms_time = ticks_to_time(abs_time, tpb, tempo)
            
            # note_on event
            if msg.type == "note_on" and msg.velocity > 0:
                note = msg.note
                freq = midi_to_freq(note)
                
                # store start time for note
                active_notes[note] = {
                    "f" : freq, 
                    "a" : ms_time
                }
                
            # note_off event
            if (msg.type == "note_off") or (msg.type == "note_on" and msg.velocity == 0):
                note = msg.note
                
                if note in active_notes:
                    # complete row with end time
                    note_data = active_notes.pop(note)
                    note_data["b"] = ms_time    # creates new key in data from dictionary index
                    events.append(note_data)    # adds to new line
                    
    # Finished processing all midi tracks (for i, track in enumerate(midi.tracks):)
    
    # Sort events in chronological order
    events.sort(key=lambda x: x["a"])    
    
    # Write to csv file
    with open(out_file, 'w', newline='') as csvfile:
        fieldnames = ["f", "a", "b"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for event in events:
            writer.writerow(event)
            
    print(f"CSV file saved as: {out_file}")
            
# file names
print()

# file_name = input("Enter the name of the .mid file you would like to convert (do not include the file type): ")
file_name = "twinkle-twinkle-little-star"
# in_file = "midi_files/" + file_name + ".mid"


midi_to_csv(file_name)