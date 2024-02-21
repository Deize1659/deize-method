import wave
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Generator

import numpy as np
import pytest

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
    channels = 2  # チャンネル数
    t = np.arange(sample_rate * duration)
    y = 0.5 * np.sin(2 * np.pi * freq * t / sample_rate)
    write = np.tile(y * 32767, (channels, 1)).T.astype(np.int16)
    ans = write.astype(np.int32)
    with wave.open(str(scope_session), "w") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(write.tobytes())
    yield (
        ans,
        (
            channels,
            sample_rate,
            sample_rate * duration,
        ),
    )
    print("\nClass scope end")


@pytest.fixture
def write_setup(scope_session: Path) -> Generator[Any, Any, Any]:
    parent_path = scope_session.parent
    write_path = parent_path / "write_test.wav"
    yield (write_path)


class TestReadWavNdarray:
    def test_read_params(self, scope_session: Path, scope_class: tuple[np.ndarray, tuple[int, ...]]) -> None:
        with ReadWavNdarray(scope_session) as rwn:
            assert rwn.channels == scope_class[1][0]
            assert rwn.rate == scope_class[1][1]
            assert rwn.frames == scope_class[1][2]

    def test_read_all(self, scope_session: Path, scope_class: tuple[np.ndarray, tuple[int, ...]]) -> None:
        with ReadWavNdarray(scope_session) as rwn:
            assert np.all(rwn.read_all() == scope_class[0])

    def test_read_frames(self, scope_session: Path, scope_class: tuple[np.ndarray, tuple[int, ...]]) -> None:
        start_pos = 10
        end_pos = 20
        read_frame = 10
        with ReadWavNdarray(scope_session) as rwn:
            assert np.all(rwn.read_frames(start_pos) == scope_class[0][start_pos:])
            assert np.all(rwn.read_frames(start_pos, end_frame=end_pos) == scope_class[0][start_pos:end_pos])
            assert np.all(
                rwn.read_frames(start_pos, read_frame=read_frame) == scope_class[0][start_pos : start_pos + read_frame]
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
    def test_write(self, write_setup: Path, scope_class: tuple[np.ndarray, tuple[int, ...]]) -> None:
        with WriteWavNdarray(write_setup, 44100, WavNdarray.INT16, 1) as wwn:
            wwn.write(scope_class[0])
        assert np.all(ReadWavNdarray(write_setup).read_all() == scope_class[0])
