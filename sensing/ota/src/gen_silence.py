#!/usr/bin/env python3
"""Generate a cf32 file containing complex zeros.

Usage:
  python3 gen_silence.py --length 1024 --out /tmp/silence.cf32

Writes raw complex32 (numpy complex64) interleaved binary.
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

import numpy as np


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Generate cf32 file of complex zeros')
    p.add_argument('--length', '-N', type=int, required=True, help='number of complex samples')
    p.add_argument('--out', '-o', default=None, help='output file path or directory (optional)')
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    if args.length < 0:
        print('length must be non-negative', file=sys.stderr)
        return 2

    # determine output path:
    # - if --out is not provided: use silence<N>.cf32 in current directory
    # - if --out is a directory: create silence<N>.cf32 inside that directory
    # - if --out is a filename: use it exactly as provided
    out = args.out
    if out is None:
        out_path = f'silence{args.length}.cf32'
    else:
        if out.endswith(os.sep) or os.path.isdir(out):
            os.makedirs(out, exist_ok=True)
            out_path = os.path.join(out, f'silence{args.length}.cf32')
        else:
            out_path = out
            d = os.path.dirname(out_path)
            if d:
                os.makedirs(d, exist_ok=True)

    data = np.zeros(args.length, dtype=np.complex64)
    data.tofile(out_path)
    print(f'Wrote {args.length} complex zeros to {out_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
