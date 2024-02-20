from ..common import Final, Optional, Path, np, queue, threading, wave


class WavNdarray:
    INT16: Final[int] = 2
    INT24: Final[int] = 3
    INT32: Final[int] = 4

    def __init__(self, wav_path: Path) -> None:
        self._wav_path = wav_path

    @property
    def path(self) -> Path:
        return self._wav_path
