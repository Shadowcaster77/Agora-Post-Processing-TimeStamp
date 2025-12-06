"""
Read a CSV file of complex numbers and plot their magnitude histogram.
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def read_complex_csv(path):
    """
    Reads a CSV file into a 2D numpy array of complex values.
    Supports arbitrary line length and commas separating entries.
    """
    complex_data = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Split by comma, strip spaces, and parse as complex
            values = []
            for token in line.split(','):
                token = token.strip()
                if not token:
                    continue
                # Ensure Python can interpret 'j' correctly
                token = token.replace('I', 'i').replace('i', 'j').replace('J', 'j')
                try:
                    values.append(complex(token))
                except ValueError:
                    # skip invalid entries gracefully
                    continue
            if values:
                complex_data.append(values)
    return np.array(complex_data, dtype=np.complex128)


def plot_magnitude_histogram(data, bins=100, normalize=False, title=None):
    """
    Plots a histogram of the magnitude (absolute value) of complex data.
    """
    magnitudes = np.abs(data).flatten()

    plt.figure(figsize=(7, 5))
    plt.hist(
        magnitudes,
        bins=bins,
        color='tab:blue',
        alpha=0.7,
        edgecolor='black',
        density=normalize,
    )
    plt.xlabel("Magnitude", fontsize=14)
    plt.ylabel("Count" if not normalize else "Density", fontsize=14)
    plt.title(title or "Histogram of Complex Magnitudes", fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("../figs/hist_complex.png", dpi=300)


def main():
    parser = argparse.ArgumentParser(description="Plot magnitude histogram of complex CSV data.")
    parser.add_argument("csv_path", help="Path to the CSV file containing complex numbers")
    parser.add_argument("--bins", type=int, default=100, help="Number of histogram bins")
    parser.add_argument("--normalize", action="store_true", help="Normalize histogram (density=True)")
    args = parser.parse_args()

    if not os.path.exists(args.csv_path):
        raise FileNotFoundError(f"File not found: {args.csv_path}")

    data = read_complex_csv(args.csv_path)
    print(f"Loaded array shape: {data.shape}")
    print(f"Example entry: {data.flat[0] if data.size > 0 else 'N/A'}")

    plot_magnitude_histogram(data, bins=args.bins, normalize=args.normalize)


if __name__ == "__main__":
    main()
