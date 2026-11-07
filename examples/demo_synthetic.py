"""Write a few SYNTHETIC vowels to WAV and extract features from them. No human recordings are used."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from scipy.io import wavfile

from voice_features import extract, synthetic_vowel

out = pathlib.Path(__file__).resolve().parent / "synthetic_wav"
out.mkdir(exist_ok=True)
cases = {
    "steady_voice": dict(jitter=0.003, shimmer=0.02, noise_db=-40),
    "more_jitter": dict(jitter=0.02, shimmer=0.02, noise_db=-40),
    "more_shimmer": dict(jitter=0.003, shimmer=0.12, noise_db=-40),
    "breathy_noisy": dict(jitter=0.003, shimmer=0.02, noise_db=-15),
}
print(f"{'case':<14} {'F0':>6} {'jitter%':>8} {'shimmer%':>9} {'HNR dB':>7} {'CPPS dB':>8} {'F1':>6} {'F2':>6}")
for name, kw in cases.items():
    x, fs = synthetic_vowel(seed=7, **kw)
    path = out / f"{name}.wav"
    wavfile.write(path, fs, (x * 32767).astype(np.int16))
    f = extract(path)
    print(f"{name:<14} {f.f0_mean_hz:6.1f} {f.jitter_local_pct:8.2f} {f.shimmer_local_pct:9.2f} "
          f"{f.hnr_db:7.1f} {f.cpps_db:8.1f} {f.f1_mean_hz:6.0f} {f.f2_mean_hz:6.0f}")
