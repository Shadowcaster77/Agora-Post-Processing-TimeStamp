"""
Read a CSV file of numbers and plot their histogram of real values.
If complex entries are present they are converted to their real part.
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def read_real_csv(path):
    """
    Reads a CSV file into a 2D numpy array of real (float) values.
    Tokens that parse as complex will be converted to their real part.
    Invalid tokens are skipped.
    """
    real_data = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            values = []
            for token in line.split(','):
                token = token.strip()
                if not token:
                    continue
                # Try float first, fall back to complex (take real part)
                try:
                    val = float(token)
                except ValueError:
                    try:
                        # normalize imaginary unit and parse
                        t = token.replace('I', 'i').replace('i', 'j').replace('J', 'j')
                        c = complex(t)
                        val = float(c.real)
                    except Exception:
                        # skip invalid entries gracefully
                        continue
                values.append(val)
            if values:
                real_data.append(values)
    return np.array(real_data, dtype=np.float64)


def plot_real_histogram(data, bins=100, normalize=False, title=None, out_path=None):
    """
    Plots a histogram of real values.
    """
    values = data.flatten()

    plt.figure(figsize=(7, 5))
    plt.hist(
        values,
        bins=bins,
        color='tab:blue',
        alpha=0.7,
        edgecolor='black',
        density=normalize,
    )
    plt.xlabel("Value", fontsize=14)
    plt.ylabel("Count" if not normalize else "Density", fontsize=14)
    plt.title(title or "Histogram of Real Values", fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    # Ensure output directory exists
    if out_path is None:
        out_dir = os.path.join(os.path.dirname(__file__), "..", "figs")
        out_path = os.path.abspath(os.path.join(out_dir, "hist_real.png"))
    else:
        out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=300)
    print(f"Saved histogram to: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Plot histogram of real CSV data (uses real part for complex tokens).")
    parser.add_argument("csv_path", help="Path to the CSV file containing numbers")
    parser.add_argument("--bins", type=int, default=100, help="Number of histogram bins")
    parser.add_argument("--normalize", action="store_true", help="Normalize histogram (density=True)")
    parser.add_argument("--out", help="Output image path (defaults to ../fig/hist_real.png)")
    args = parser.parse_args()

    if not os.path.exists(args.csv_path):
        raise FileNotFoundError(f"File not found: {args.csv_path}")

    data = read_real_csv(args.csv_path)
    print(f"Loaded array shape: {data.shape}")
    print(f"Example entry: {data.flat[0] if data.size > 0 else 'N/A'}")
    plot_real_histogram(data, bins=args.bins, normalize=args.normalize, out_path=args.out)


if __name__ == "__main__":
    main()
