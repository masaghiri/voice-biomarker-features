"""Synthetic sustained vowels for testing, so no human recordings are ever needed in this repository."""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter


def _resonator(freq: float, bandwidth: float, fs: int):
    r = np.exp(-np.pi * bandwidth / fs)
    theta = 2 * np.pi * freq / fs
    a = [1, -2 * r * np.cos(theta), r**2]
    b = [1 - r]
    return b, a


def synthetic_vowel(f0: float = 120.0, duration: float = 1.5, fs: int = 16000,
                    jitter: float = 0.005, shimmer: float = 0.03,
                    formants=((700, 80), (1200, 90), (2600, 120)), noise_db: float = -35.0,
                    seed: int = 0) -> tuple[np.ndarray, int]:
    """Glottal pulse train with controlled jitter and shimmer, shaped by formant resonators.

    jitter and shimmer are relative cycle-to-cycle perturbations (0.005 = 0.5%).
    Returns (signal scaled to +/-0.9, sampling rate).
    """
    rng = np.random.default_rng(seed)
    n = int(duration * fs)
    source = np.zeros(n)
    t = 0.0
    while t < duration:
        idx = int(t * fs)
        if idx >= n:
            break
        source[idx] = 1.0 + shimmer * rng.standard_normal()
        period = (1.0 / f0) * (1.0 + jitter * rng.standard_normal())
        t += max(period, 0.5 / f0)
    # glottal-like low-pass shaping
    signal = lfilter([1.0], [1.0, -0.97], source)
    for freq, bw in formants:
        b, a = _resonator(freq, bw, fs)
        signal = lfilter(b, a, signal)
    signal = signal / np.max(np.abs(signal))
    signal = signal + 10 ** (noise_db / 20) * rng.standard_normal(n)
    signal = 0.9 * signal / np.max(np.abs(signal))
    return signal.astype(np.float64), fs
