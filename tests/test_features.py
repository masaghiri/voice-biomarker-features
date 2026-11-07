import math

import parselmouth
import pytest

from voice_features import extract, synthetic_vowel


def _sound(**kw):
    x, fs = synthetic_vowel(**kw)
    return parselmouth.Sound(x, sampling_frequency=fs)


def test_pitch_recovered():
    f = extract(_sound(f0=120.0))
    assert f.f0_mean_hz == pytest.approx(120.0, rel=0.03)


def test_first_formant_near_target():
    f = extract(_sound(f0=120.0, formants=((700, 80), (1200, 90), (2600, 120))))
    assert 550 < f.f1_mean_hz < 850


def test_more_jitter_gives_higher_jitter():
    low = extract(_sound(jitter=0.002, seed=1)).jitter_local_pct
    high = extract(_sound(jitter=0.02, seed=1)).jitter_local_pct
    assert high > low


def test_more_shimmer_gives_higher_shimmer():
    low = extract(_sound(shimmer=0.01, seed=2)).shimmer_local_pct
    high = extract(_sound(shimmer=0.15, seed=2)).shimmer_local_pct
    assert high > low


def test_more_noise_lowers_hnr():
    clean = extract(_sound(noise_db=-45, seed=3)).hnr_db
    noisy = extract(_sound(noise_db=-12, seed=3)).hnr_db
    assert clean > noisy


def test_all_fields_are_numbers():
    f = extract(_sound())
    for k, v in f.as_dict().items():
        if k != "file":
            assert isinstance(v, float) and not math.isnan(v), k
