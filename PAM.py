from scipy.io import wavfile
from datetime import datetime
from pathlib import PosixPath
from datetime import date

class PAMFile:
    def __init__(self, path: PosixPath, unit: str, dt: date):
        self.path = path
        self.unit = unit
        self.dt = dt
        self.wave = None
        self.rate = None
        self._read = False

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
