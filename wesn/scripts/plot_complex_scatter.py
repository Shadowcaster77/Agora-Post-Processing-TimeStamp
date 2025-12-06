"""
Plot complex CSV data on a symmetric complex plane with larger ticks.
Supports both 'i' and 'j' complex notations.
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def read_complex_csv(path):
    """Reads a CSV file into a 2D numpy array of complex values."""
    complex_data = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = []
            for token in line.split(','):
                token = token.strip()
                if not token:
                    continue
                token = token.replace('I', 'i').replace('i', 'j').replace('J', 'j')
                try:
                    row.append(complex(token))
                except ValueError:
                    print(f"Warning: Skipping invalid entry: {token}")
            if row:
                complex_data.append(row)
    return np.array(complex_data, dtype=np.complex128)


def plot_complex_plane(data, title=None, alpha=0.6, color='tab:blue', margin=0.05, tick_size=16):
    """Plots all complex numbers on the complex plane with symmetric axes."""
    z = data.flatten()
    re = z.real
    im = z.imag

    # === Compute symmetric limits ===
    max_range = max(abs(re).max(), abs(im).max())
    if max_range == 0:
        max_range = 1.0
    limit = max_range * (1 + margin)

    plt.figure(figsize=(6, 6))
    plt.scatter(re, im, color=color, alpha=alpha, s=10, edgecolor='none')

    # Axes and labels
    plt.axhline(0, color='gray', lw=1, linestyle='--', alpha=0.7)
    plt.axvline(0, color='gray', lw=1, linestyle='--', alpha=0.7)
    plt.xlabel("Real part", fontsize=18)
    plt.ylabel("Imaginary part", fontsize=18)
    plt.title(title or "Complex Plane Scatter", fontsize=20, pad=12)

    # Set symmetric limits and equal aspect
    # plt.xlim(-limit, limit)
    # plt.ylim(-limit, limit)
    # plt.axis('equal')

    # === Larger ticks ===
    plt.xticks(fontsize=tick_size)
    plt.yticks(fontsize=tick_size)
    plt.tick_params(width=1.5, length=6)

    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig("../figs/complex_scatter.png", dpi=300)


def main():
    parser = argparse.ArgumentParser(description="Plot complex CSV data on a symmetric complex plane with large ticks.")
    parser.add_argument("csv_path", help="Path to the CSV file containing complex numbers")
    parser.add_argument("--alpha", type=float, default=0.6, help="Point transparency (0–1)")
    parser.add_argument("--color", default="tab:blue", help="Point color")
    parser.add_argument("--margin", type=float, default=0.05, help="Fractional margin around max range")
    parser.add_argument("--tick_size", type=int, default=16, help="Font size for tick labels")
    args = parser.parse_args()

    if not os.path.exists(args.csv_path):
        raise FileNotFoundError(f"File not found: {args.csv_path}")

    data = read_complex_csv(args.csv_path)
    print(f"Loaded array shape: {data.shape}")
    if data.size > 0:
        print(f"Example entry: {data.flat[0]}")

    plot_complex_plane(data, title=os.path.basename(args.csv_path),
                       alpha=args.alpha, color=args.color,
                       margin=args.margin, tick_size=args.tick_size)


if __name__ == "__main__":
    main()