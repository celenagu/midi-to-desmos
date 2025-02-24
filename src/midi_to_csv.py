import os
import csv
from mido import MidiFile

# Convert midi note to frequency
def midi_to_freq(n):
    return 440.0*2**((n-69) / 12.0)

def ticks_to_time(ticks, tpb, tempo):
    us_per_tick = tempo / tpb
    return ticks * us_per_tick / 1000000.0

def midi_to_csv(file_name):
    in_file = "midi_files/" + file_name + ".mid"
    out_file = "output/" + file_name + ".csv"
    log_file = "output/" + file_name + "_log.txt"
    
    print(f"Reading midi file {in_file}")
    
    # Initialize log data
    log_data = f"Log for MIDI file: {in_file}\n\n"
    
    # load in midi file
    midi = MidiFile(in_file)
    events = []
    
    # Display general MIDI info
    print(f"Number of tracks: {len(midi.tracks)}")
    tpb = midi.ticks_per_beat
    print(f"Ticks per beat: {tpb}")
    log_data += f"Number of tracks: {len(midi.tracks)}\n"
    log_data += f"Ticks per beat: {tpb}\n\n"
    
    # Get initial tempo (default 120 BPM, 500000 us/beat)
    tempo = 500000
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                print(f"Tempo Found: {tempo}")
                break
    
    # Track currently active notes
    active_notes = {}

    # Process each track and event
    for i, track in enumerate(midi.tracks):
        print(f"\nProcessing Track {i}: {track.name}")
        log_data += f"\nProcessing Track {i}: {track.name}\n"
        abs_time = 0
        
        for msg in track:
            print(msg)
            log_data += str(msg) + "\n"  # Accumulate the msg in log_data
            abs_time += msg.time
            ms_time = ticks_to_time(abs_time, tpb, tempo)
            
            # note_on event
            if msg.type == "note_on" and msg.velocity > 0:
                note = msg.note + 12
                freq = midi_to_freq(note)
                
                # store start time for note
                active_notes[note] = {
                    "f" : freq, 
                    "a" : ms_time
                }
                
            # note_off event
            if (msg.type == "note_off") or (msg.type == "note_on" and msg.velocity == 0):
                note = msg.note + 12
                
                if note in active_notes:
                    # complete row with end time
                    note_data = active_notes.pop(note)
                    note_data["b"] = ms_time    # creates new key in data from dictionary index
                    events.append(note_data)    # adds to new line  

    # Finished processing all midi tracks (for i, track in enumerate(midi.tracks):)
    
    # Sort events in chronological order
    events.sort(key=lambda x: x["a"]) 

    # Ensure output directory exists
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Write to csv file
    with open(out_file, 'w', newline='') as csvfile:
        fieldnames = ["e", "a", "b", "f"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        num = 0
        for event in events:
            writer.writerow({"e": num, "a": event["a"], "b": event["b"], "f": event["f"]})
            num += 1
            
    # Write all accumulated logs to the log file at once
    with open(log_file, 'w') as log:
        log.write(log_data)
        
    print(f"CSV file saved as: {out_file}")
            
# file names
print()
# file_name = input("Enter the name of the .mid file you would like to convert (do not include the file extension): ")
file_name = "twinkle-twinkle-little-star"
# file_name = "Beethoven - Fur Elise"
# file_name = "canon-3"

midi_to_csv(file_name)