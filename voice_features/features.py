"""Acoustic voice features computed with Praat (via parselmouth).

Features follow those used in voice-and-diabetes research, for example:
Saghiri MA, et al. Exploring the impact of type II diabetes mellitus on voice quality.
Eur Arch Otorhinolaryngol. 2024;281(5):2707-16. https://doi.org/10.1007/s00405-024-08485-4

Voice onset time (VOT), also used in that study, needs consonant-vowel segmentation and is not
computed automatically here.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path

import parselmouth
from parselmouth.praat import call


@dataclass
class VoiceFeatures:
    file: str
    duration_s: float
    f0_mean_hz: float
    f0_sd_hz: float
    jitter_local_pct: float
    shimmer_local_pct: float
    hnr_db: float
    cpps_db: float
    f1_mean_hz: float
    f2_mean_hz: float

    def as_dict(self) -> dict:
        return asdict(self)


def _nan_if_undefined(x) -> float:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return float("nan")
    return x if math.isfinite(x) else float("nan")


def extract(source: str | Path | parselmouth.Sound, f0_min: float = 75.0, f0_max: float = 500.0,
            max_formant_hz: float = 5500.0) -> VoiceFeatures:
    """Compute features for a sustained vowel or short speech recording.

    f0_min / f0_max bound the pitch search (75-500 Hz covers most adult voices); max_formant_hz is
    Praat's formant ceiling (about 5000 Hz for adult male and 5500 Hz for adult female voices).
    """
    sound = source if isinstance(source, parselmouth.Sound) else parselmouth.Sound(str(source))
    name = "" if isinstance(source, parselmouth.Sound) else Path(source).name
    if sound.n_channels > 1:
        sound = sound.convert_to_mono()

    pitch = sound.to_pitch(time_step=0.01, pitch_floor=f0_min, pitch_ceiling=f0_max)
    f0_mean = call(pitch, "Get mean", 0, 0, "Hertz")
    f0_sd = call(pitch, "Get standard deviation", 0, 0, "Hertz")

    points = call(sound, "To PointProcess (periodic, cc)", f0_min, f0_max)
    jitter = call(points, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    shimmer = call([sound, points], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0_min, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)

    cepstrogram = call(sound, "To PowerCepstrogram", 60, 0.002, 5000, 50)
    cpps = call(cepstrogram, "Get CPPS", True, 0.02, 0.0005, 60, 330, 0.05, "Parabolic", 0.001, 0,
                "Exponential decay", "Robust")

    formants = sound.to_formant_burg(time_step=0.01, max_number_of_formants=5,
                                     maximum_formant=max_formant_hz)
    f1 = call(formants, "Get mean", 1, 0, 0, "hertz")
    f2 = call(formants, "Get mean", 2, 0, 0, "hertz")

    return VoiceFeatures(
        file=name,
        duration_s=round(sound.duration, 3),
        f0_mean_hz=_nan_if_undefined(f0_mean),
        f0_sd_hz=_nan_if_undefined(f0_sd),
        jitter_local_pct=100 * _nan_if_undefined(jitter),
        shimmer_local_pct=100 * _nan_if_undefined(shimmer),
        hnr_db=_nan_if_undefined(hnr),
        cpps_db=_nan_if_undefined(cpps),
        f1_mean_hz=_nan_if_undefined(f1),
        f2_mean_hz=_nan_if_undefined(f2),
    )
