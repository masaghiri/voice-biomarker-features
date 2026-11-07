# Voice biomarker features

Open, tested code for the acoustic voice measures used in voice-and-diabetes research, computed with [Praat](https://www.fon.hum.uva.nl/praat/) through [parselmouth](https://parselmouth.readthedocs.io).

In a matched study of 60 adults, 30 with type 2 diabetes, voices recorded on ordinary smartphones differed in five of seven acoustic features (fundamental frequency, jitter, shimmer, cepstral peak prominence and harmonics-to-noise ratio; p < 0.05), and shimmer was the strongest predictor ([Saghiri et al., Eur Arch Otorhinolaryngol 2024](https://doi.org/10.1007/s00405-024-08485-4)). This repository makes the feature step reproducible so others can check and extend it.

## Features

| Column | Meaning | Praat method |
|---|---|---|
| `f0_mean_hz`, `f0_sd_hz` | Pitch (fundamental frequency) and its variability | `To Pitch` |
| `jitter_local_pct` | Cycle-to-cycle variation in period | `PointProcess (periodic, cc)` → `Get jitter (local)` |
| `shimmer_local_pct` | Cycle-to-cycle variation in amplitude | `Get shimmer (local)` |
| `hnr_db` | Harmonics-to-noise ratio | `To Harmonicity (cc)` |
| `cpps_db` | Smoothed cepstral peak prominence | `To PowerCepstrogram` → `Get CPPS` |
| `f1_mean_hz`, `f2_mean_hz` | First and second formants | `To Formant (burg)` |

Voice onset time, also used in the 2024 study, needs consonant–vowel segmentation and is not computed automatically.

## Quick start

```bash
pip install praat-parselmouth numpy scipy
git clone https://github.com/masaghiri/voice-biomarker-features
cd voice-biomarker-features
python examples/demo_synthetic.py                    # synthetic vowels, no human data
python -m voice_features my_vowel.wav --out features.csv
```

```python
from voice_features import extract
print(extract("my_vowel.wav").as_dict())
```

Output of the synthetic demo:

```
case               F0  jitter%  shimmer%  HNR dB  CPPS dB     F1     F2
steady_voice    120.0     0.40      2.10    23.0     16.6    698   1187
more_jitter     120.2     1.81      4.53    13.7     13.4    697   1185
more_shimmer    120.0     0.43     11.37    19.3     15.2    699   1189
breathy_noisy   120.0     0.70      8.69     3.0      9.4    829   1919
```

The tests check that the code recovers known pitch and formants from synthetic vowels and that jitter, shimmer and noise move each measure in the expected direction.

```bash
pip install pytest
python -m pytest -q
```

## Recording tips

Use a sustained vowel ("ah") of at least two seconds, a quiet room, and the same device and distance for every recording. Set `--f0-min` and `--f0-max` to the speaker's range, and `--max-formant` to about 5000 Hz for adult male and 5500 Hz for adult female voices.

## Status and use

Research software, version 0.1. **Not a diagnostic test and not for clinical decisions.** This repository contains no human recordings; all examples are synthetic. Do not commit patient recordings to any public repository.

## Citation

See [`CITATION.cff`](CITATION.cff). Author: M. Ali Saghiri, MS, PhD ([ORCID 0000-0002-5064-7828](https://orcid.org/0000-0002-5064-7828)).

## License

MIT. See [`LICENSE`](LICENSE).
