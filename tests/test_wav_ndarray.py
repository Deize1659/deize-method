from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Generator

import numpy as np
import pytest
from scipy.io.wavfile import write

from my_method.wav_ndarray.wav_ndarray import (
    ReadWavNdarray,
    WavNdarray,
    WriteWavNdarray,
)


@pytest.fixture(scope="session")
def scope_session() -> Generator[Any, Any, Any]:
    print("\nSession scope")
    with TemporaryDirectory() as tmp_dir:
        print(f"Temporary directory: {tmp_dir}")
        path = Path(tmp_dir) / "1kHz_sine_wave.wav"
        yield (path)
        print("\nSession scope end")


@pytest.fixture(scope="class")
def scope_class(scope_session: Path) -> Generator[Any, Any, Any]:
    print("\nClass scope")
    sample_rate = 44100  # サンプルレート (Hz)
    freq = 1000  # 周波数 (Hz)
    duration = 10  # 持続時間 (秒)
    t = np.arange(sample_rate * duration)
    y = 0.5 * np.sin(2 * np.pi * freq * t / sample_rate)
    ans = (y * 32767).astype(np.int32)
    write(str(scope_session), sample_rate, ans.astype(np.int16))
    yield (ans)
    print("\nClass scope end")


@pytest.fixture
def write_setup(scope_session: Path) -> Generator[Any, Any, Any]:
    parent_path = scope_session.parent
    write_path = parent_path / "write_test.wav"
    yield (write_path)


class TestReadWavNdarray:
    def test_read_all(self, scope_session: Path, scope_class: np.ndarray) -> None:
        with ReadWavNdarray(scope_session) as rwn:
            assert rwn.width == WavNdarray.INT16
            assert rwn.channels == 1
            assert rwn.rate == 44100
            assert rwn.frames == 441000
            assert np.all(rwn.read_all() == scope_class)

    def test_read_frames(self, scope_session: Path, scope_class: np.ndarray) -> None:
        start_pos = 10
        end_pos = 20
        read_frame = 10
        with ReadWavNdarray(scope_session) as rwn:
            assert np.all(rwn.read_frames(start_pos) == scope_class[start_pos:])
            assert np.all(rwn.read_frames(start_pos, end_frame=end_pos) == scope_class[start_pos:end_pos])
            assert np.all(
                rwn.read_frames(start_pos, read_frame=read_frame) == scope_class[start_pos : start_pos + read_frame]
            )
            with pytest.raises(ValueError):
                rwn.read_frames(start_pos, read_frame=-1)
            with pytest.raises(ValueError):
                rwn.read_frames(start_pos, end_frame=start_pos)
            with pytest.raises(ValueError):
                rwn.read_frames(start_pos, end_frame=end_pos, read_frame=read_frame)
            with pytest.raises(ValueError):
                rwn.read_frames(start_pos, end_frame="end_pos", read_frame=read_frame)  # type: ignore


class TestWriteWavNdarray:
    def test_write(self, write_setup: Path, scope_class: np.ndarray) -> None:
        with WriteWavNdarray(write_setup, 44100, WavNdarray.INT16, 1) as wwn:
            wwn.write(scope_class)
        assert np.all(ReadWavNdarray(write_setup).read_all() == scope_class)
