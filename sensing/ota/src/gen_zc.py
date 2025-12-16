#!/usr/bin/env python3
"""Generate a Zadoff-Chu (ZC) sequence and write as complex float32 (cf32).

Usage examples:
  python3 gen_zc.py --length 63 --root 1 --out /tmp/zc63.cf32
  python3 gen_zc.py --length 13 --root 2 --print

The output file (when provided) is raw interleaved complex32 (I,Q) binary data
matching numpy dtype `np.complex64` (little-endian on typical Linux).
"""
from __future__ import annotations

import argparse
import math
import sys
from typing import Optional

import numpy as np


def zc_sequence(length: int, root: int) -> np.ndarray:
    """Return a Zadoff-Chu sequence of given length and root as complex64.

    For even `length` use phase -pi * root * n^2 / N.
    For odd `length` use phase -pi * root * n*(n+1) / N.
    Root must be coprime with length.
    """
    if length <= 0:
        raise ValueError("length must be positive")
    if math.gcd(root, length) != 1:
        raise ValueError(f"root ({root}) must be coprime with length ({length})")

    n = np.arange(length, dtype=np.int64)
    N = length
    if N % 2 == 0:
        phase = -np.pi * root * (n.astype(np.float64) ** 2) / float(N)
    else:
        phase = -np.pi * root * (n.astype(np.float64) * (n + 1)) / float(N)

    seq = np.exp(1j * phase).astype(np.complex64)
    return seq


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate Zadoff-Chu sequence (cf32)")
    p.add_argument("--length", "-N", type=int, required=True,
                   help="sequence length N")
    p.add_argument("--root", "-r", type=int, default=1,
                   help="root (integer coprime with N)")
    p.add_argument("--out", "-o", type=str, default=None,
                   help="output file path (raw cf32 binary)")
    p.add_argument("--print", action="store_true",
                   help="print first few complex samples to stdout")
    p.add_argument("--count", "-c", type=int, default=8,
                   help="how many samples to print when --print used")
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    try:
        seq = zc_sequence(args.length, args.root)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if args.print:
        cnt = min(args.count, seq.size)
        for i in range(cnt):
            s = seq[i]
            print(f"{i}: {s.real:.6f} + {s.imag:.6f}j")

    if args.out:
        # Write raw complex32 binary (interleaved float32 I,Q)
        seq.tofile(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
