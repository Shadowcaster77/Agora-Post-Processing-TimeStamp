#!/usr/bin/env python3
"""Plot a cf32 file: I/Q linear plots, constellation, and correlation with ZC
reference.

Saves PNGs to an output directory (default /tmp).

Usage:
  python3 plot_zc.py --file /path/to/signal.cf32 --length 63 --root 1 --outdir /tmp/plots

This script expects the input file to be raw complex32 (numpy complex64)
interleaved binary (I,Q floats). It will generate three PNGs: `iq_linear.png`,
`constellation.png`, and `correlation.png` in the output directory.
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from typing import Optional

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_cf32(path: str) -> np.ndarray:
    data = np.fromfile(path, dtype=np.complex64)
    return data


def zc_sequence(length: int, root: int) -> np.ndarray:
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


def plot_iq_linear(seq: np.ndarray, outpath: str, title: str = "I/Q samples") -> None:
    plt.figure(figsize=(10, 4))
    t = np.arange(seq.size)
    plt.plot(t, seq.real, label='I', lw=1)
    plt.plot(t, seq.imag, label='Q', lw=1)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_constellation(seq: np.ndarray, outpath: str, title: str = 'Constellation') -> None:
    plt.figure(figsize=(5, 5))
    plt.scatter(seq.real, seq.imag, s=8)
    plt.axhline(0, color='gray', lw=0.6)
    plt.axvline(0, color='gray', lw=0.6)
    plt.xlabel('I')
    plt.ylabel('Q')
    plt.title(title)
    plt.grid(True)
    plt.gca().set_aspect('equal', 'box')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def correlate_and_plot(sig: np.ndarray, ref: np.ndarray, outpath: str, title: str = 'Correlation') -> None:
    # linear cross-correlation: corr[k] = sum_n sig[n] * conj(ref[n-k])
    corr = np.correlate(sig, ref.conj(), mode='full')
    mags = np.abs(corr)
    lags = np.arange(-ref.size + 1, sig.size)

    plt.figure(figsize=(10, 4))
    plt.plot(lags, mags)
    peak_idx = np.argmax(mags)
    peak_lag = lags[peak_idx]
    peak_val = mags[peak_idx]
    plt.plot(peak_lag, peak_val, 'ro')
    plt.annotate(f'peak lag={int(peak_lag)}, mag={peak_val:.3f}',
                 xy=(peak_lag, peak_val), xytext=(10, -10),
                 textcoords='offset points')
    plt.xlabel('Lag')
    plt.ylabel('Correlation magnitude')
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description='Plot cf32 I/Q data, constellation, and ZC correlation')
    p.add_argument('--file', '-f', required=True,
                   help='input cf32 file (complex64 raw)')
    p.add_argument('--length', '-N', type=int, default=63,
                   help='ZC reference length')
    p.add_argument('--root', '-r', type=int, default=1,
                   help='ZC root (coprime with N)')
    p.add_argument('--outdir', '-o', default='/tmp',
                   help='output directory to save PNGs')
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    if not os.path.isfile(args.file):
        print(f'Input file not found: {args.file}', file=sys.stderr)
        return 2
    os.makedirs(args.outdir, exist_ok=True)

    sig = read_cf32(args.file)
    if sig.size == 0:
        print('Input file contains no samples', file=sys.stderr)
        return 3

    # plot entire file
    plot_samples = sig

    base = os.path.basename(args.file)
    name = os.path.splitext(base)[0]
    iq_path = os.path.join(args.outdir, f'{name}_iq_linear.png')
    const_path = os.path.join(args.outdir, f'{name}_constellation.png')
    corr_path = os.path.join(args.outdir, f'{name}_correlation.png')

    plot_iq_linear(plot_samples, iq_path,
                   title=f'I/Q ({plot_samples.size} samples)')
    plot_constellation(plot_samples, const_path,
                       title=f'Constellation ({plot_samples.size} samples)')

    # build ZC reference and correlate
    try:
        ref = zc_sequence(args.length, args.root)
    except ValueError as e:
        print(f'Invalid ZC params: {e}', file=sys.stderr)
        return 4

    # correlate full signal with reference
    correlate_and_plot(
        sig, ref, corr_path,
        title=f'Correlation with ZC N={args.length} root={args.root}')

    print('Saved:', iq_path, const_path, corr_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
