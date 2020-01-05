from scipy.io import wavfile
from datetime import datetime
from pathlib import PosixPath
from datetime import date
import numpy as np
from LTSA import RawLTSA

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
        self._ltsa = None

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

    def extract_label_wave(self, label: PAMLabel, padding: float = 1):
        rate, wave = self.read()
        start = int(np.floor((label.start - padding) * rate))
        end = int(np.ceil((label.end + padding) * rate))
        return wave[start:end]

    def save_label_wave(self, filename: str, label: PAMLabel, padding: float = 1):
        rate, wave = self.read()
        label_wave = self.extract_label_wave(label, padding)
        wavfile.write(filename, rate, label_wave)

    def showLTSA(self):
        self._LTSA()
        self._ltsa.show()

    def saveLTSA(self, filename: str):
        self._LTSA()
        self._ltsa.save(filename)

    def _LTSA(self):
        if not self._ltsa:
            # these params should prbly be modified based on the rate..?
            params = {'div_len': 22050,
                      'subdiv_len': 4096,
                      'nfft': 4096,
                      'noverlap': 1000}
            rate, wave = self.read()
            self._ltsa = RawLTSA(wave, rate)
            self._ltsa.set_params(params)
            self._ltsa()
            self._ltsa.crop(fmax=6000)

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
