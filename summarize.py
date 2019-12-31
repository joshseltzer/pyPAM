from pathlib import Path
from argparse import ArgumentParser
import pandas as pd
from datetime import datetime
from PAM import PAMFile

# Options
date_format = '%Y%m%d'
time_format = '%H%M'
unit_slice = slice(5, 7)    # slice unit from filename
date_slice = slice(8, 16)   # slice date from filename
time_slice = slice(17, 21)  # slice time from filename

# Parse arguments
argparser = ArgumentParser()
argparser.add_argument("dir", help="specify the dir to load your files from")
argparser.add_argument("ext", help="specify the extension for your files",
    nargs='?', default='wav')
argparser.parse_args()
args = argparser.parse_args()

# Construct PAMFiles from filepaths
pamfiles = []
for filepath in Path(args.dir).rglob(f'*.{args.ext}'):
    stem = filepath.stem
    unit = stem[unit_slice]
    datestr = stem[date_slice]
    timestr = stem[time_slice]
    dt = datetime.strptime(datestr + timestr, date_format + time_format)
    pamf = PAMFile(filepath, unit, dt)
    pamfiles.append(pamf)

for pamf in pamfiles:
    print(pamf)


# df = pd.DataFrame(filenames, columns = ['Filepath'])
# df['Stem'] = df['Filepath'].apply(lambda fp: fp.stem)
