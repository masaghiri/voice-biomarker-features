"""Command line: python -m voice_features recording1.wav recording2.wav --out features.csv"""
import argparse
import csv
import sys

from .features import extract


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m voice_features",
                                 description="Compute acoustic voice features for WAV files.")
    ap.add_argument("wav", nargs="+", help="audio files (sustained vowel recommended)")
    ap.add_argument("--out", help="CSV file to write (default: print to screen)")
    ap.add_argument("--f0-min", type=float, default=75.0)
    ap.add_argument("--f0-max", type=float, default=500.0)
    ap.add_argument("--max-formant", type=float, default=5500.0)
    args = ap.parse_args(argv)

    rows = [extract(p, args.f0_min, args.f0_max, args.max_formant).as_dict() for p in args.wav]
    out = open(args.out, "w", newline="", encoding="utf-8") if args.out else sys.stdout
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    if args.out:
        out.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
