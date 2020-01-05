from pathlib import Path
from argparse import ArgumentParser
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from PAM import PAMFile, PAMLabel

# Options (based on our SWIFT filename configuration)
date_format = '%Y%m%d'
time_format = '%H%M'
fn_prefix = "SWIFT"
unit_slice = slice(5, 7)    # slice unit from filename
date_slice = slice(8, 16)   # slice date from filename
time_slice = slice(17, 21)  # slice time from filename

# Parse arguments
argparser = ArgumentParser()
argparser.add_argument("dir", help="specify the dir to load your files from")
argparser.add_argument("ext", help="specify the extension for your files",
    nargs='?', default='wav')
argparser.add_argument("db", help="specify the filepath for the CSV db")
argparser.parse_args()
args = argparser.parse_args()

# Construct PAMFiles from filepaths
pamfiles = []
for filepath in Path(args.dir).rglob(f'{fn_prefix}*.{args.ext}'):
    stem = filepath.stem
    unit = stem[unit_slice]
    datestr = stem[date_slice]
    timestr = stem[time_slice]
    dt = datetime.strptime(datestr + timestr, date_format + time_format)
    pamf = PAMFile(filepath, unit, dt)
    pamfiles.append(pamf)

# Load in data from database
csv = pd.read_csv(args.db)
for index, row in csv.iterrows():
    try:
        pamf = [ pamf for pamf in pamfiles if pamf == row['Filename'] ][0]
    except:
        print("Could not find PAMFile for database entry:", row['Filename'])
        continue
    label = PAMLabel(row['Taxon'], row['Type'], row['Subtype'], row['Start (s)'], row['End (s)'])
    pamf.add_label(label)


labeledpams = [ p for p in pamfiles if len(p.labels) ]

# visualize all labels in random pam
randpam = np.random.choice(labeledpams)
hootwaves = [ randpam.extract_label_wave(label, 0.5) for label in randpam.labels ]
for hw in hootwaves:
  Pxx, freqs, bins, im = plt.specgram(hw, window=np.hamming(2048), NFFT=2048, Fs=48000, noverlap=0)
  x1, x2, y1, y2 = plt.axis()
  plt.axis((x1, x2, 100, 500))
  plt.show()

# for pamf in pamfiles:
#     print(pamf)

df = pd.DataFrame(pamfiles, columns = ['PAMFile'])
