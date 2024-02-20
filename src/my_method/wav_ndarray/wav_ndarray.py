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


class ReadWavNdarray(WavNdarray):
    """
    WAVファイルを読み込み、NumPy配列として返すクラス。

    Parameters
    ----------
    WavNdarray : _type_
        親クラス
    """

    def __init__(self, wav_path: Path) -> None:
        super().__init__(wav_path)
        self._rf = wave.open(str(wav_path), "rb")
        self._width = self._rf.getsampwidth()
        self._channels = self._rf.getnchannels()
        self._rate = self._rf.getframerate()
        self._frames = self._rf.getnframes()

    def __del__(self) -> None:
        self.read_end()

    def __enter__(self) -> "ReadWavNdarray":
        return self

    def __exit__(self, exc_type: str, exc_value: str, traceback: str) -> None:
        if exc_type is not None:
            print(exc_type, exc_value, traceback)
        self.read_end()

    @property
    def width(self) -> int:
        return self._width

    @property
    def channels(self) -> int:
        return self._channels

    @property
    def rate(self) -> int:
        return self._rate

    @property
    def frames(self) -> int:
        return self._frames

    def read_all(self) -> np.ndarray:
        """
        WAVファイルの全フレームを読み込み、NumPy配列として返します。

        Returns
        -------
        np.ndarray
            NumPy配列
        """
        self._rf.setpos(0)
        return self._byte_to_ndarray(self._rf.readframes(self._frames))

    def read_frames(
        self, start_frame: int, end_frame: Optional[int] = None, read_frame: Optional[int] = None
    ) -> np.ndarray:
        """
        指定した範囲のフレームを読み込み、NumPy配列として返します。\n
        end_frame と read_frame は同時にセットできません。\n
        end_frame と read_frame をセットしない場合、start_frame から最後まで読み込みます。

        Parameters
        ----------
        start_frame : int
            読み込み開始フレーム
        end_frame : Optional[int], optional
            読み込み終了フレーム, by default None
        read_frame : Optional[int], optional
            読み込みフレーム数, by default None

        Returns
        -------
        np.ndarray
            NumPy配列

        Raises
        ------
        ValueError
            end_frame と read_frame が同時にセットされている場合
        ValueError
            end_frame が start_frame より小さい場合
        ValueError
            read_frame が負の値の場合
        """
        if end_frame is None and read_frame is None:
            read_frame = self._frames - start_frame
        elif end_frame is not None and read_frame is not None:
            raise ValueError("end_frame と read_frame は同時にセットできません")
        elif end_frame is not None and isinstance(end_frame, int):
            if end_frame <= start_frame:
                raise ValueError("end_frame は start_frame より大きい必要があります")
            read_frame = end_frame - start_frame
        elif read_frame is not None and isinstance(read_frame, int):
            if read_frame < 0:
                raise ValueError("read_frame は 0以上である必要があります")
        else:
            raise ValueError("引数が不正です")
        self._rf.setpos(start_frame)
        return self._byte_to_ndarray(self._rf.readframes(read_frame))

    def _byte_to_ndarray(self, byte: bytes) -> np.ndarray:
        """
        bytes型をNumPy配列に変換します。

        Parameters
        ----------
        byte : bytes
            wavデータ

        Returns
        -------
        np.ndarray
            音声レベル配列
        """
        if self._width == self.INT16 or self._width == self.INT24:
            array = np.frombuffer(memoryview(byte), dtype=np.int8).reshape(-1, self._width)
            if self._width == self.INT24:
                array = np.insert(array, 3, 0, axis=1)
            elif self._width == self.INT16:
                array = np.insert(array, 2, 0, axis=1)
                array = np.insert(array, 3, 0, axis=1)
            condition = array[:, self._width - 1] < 0
            array[condition, self._width :] = 0xFF
            byte = array.tobytes()
        return np.frombuffer(memoryview(byte), dtype=np.int32)

    def read_end(self) -> None:
        """
        WAVファイルの読み込みを終了し、リソースを解放します。
        """
        self._rf.close()
