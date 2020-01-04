from scipy.io import wavfile
from datetime import datetime
from pathlib import PosixPath
from datetime import date

class PAMLabel:
    def __init__(self, taxon: str, type: str, subtype: str, start: float, end: float):
        self.taxon = taxon
        self.type = type
        self.subtype = subtype
        self.start = start
        self.end = end

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"PAM label: Taxon={self.taxon}, Type={self.type}, Subtype={self.subtype}, Time={self.start}-{self.end}"

class PAMFile:
    def __init__(self, path: PosixPath, unit: str, dt: date):
        self.path = path
        self.unit = unit
        self.dt = dt
        self.wave = None
        self.rate = None
        self._read = False
        self.labels = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"PAM object from {self.__starttime__()} @ Unit #{self.unit}"

    def __starttime__(self):
        return datetime.strftime(self.dt, '%a %b %d, %Y, %H:%M')

    def read(self):
        if not self._read:
            self.rate, self.wave = wavfile.read(self.path)
            self._read = True
        return self.rate, self.wave

    def add_label(self, label: PAMLabel):
        self.labels.append(label)
        print(self.labels)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.path.stem == other.path.stem
        else:
            return self.path.stem == other

    def __ne__(self, other):
        return not self.__eq__(other)

    # def mfcc(self):
    #     rate, wave = self.read()
    #     return mfcc(wave, samplerate=rate)
    #
