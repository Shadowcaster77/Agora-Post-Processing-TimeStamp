import argparse
import glob
import os
import time
import numpy as np
import matplotlib.pyplot as plt


def get_latest_csv(folder):
    pattern = os.path.join(folder, "*.csv")
    files = glob.glob(pattern)
    if not files:
        return None
    latest = max(files, key=os.path.getmtime)
    return latest


def load_iq_from_csv(path):
    # fast load assuming plain numeric CSV with commas and no header
    # read first line to detect number of columns (handles 2xN row format)
    try:
        with open(path, "r") as f:
            first_line = f.readline()
            # if file starts with a blank line, keep reading until a non-empty
            if first_line.strip() == "":
                for _ in range(5):
                    first_line = f.readline()
                    if first_line.strip() != "":
                        break
            ncols = first_line.count(",") + 1 if first_line.strip() != "" else 0
    except Exception:
        ncols = 0

    try:
        flat = np.fromfile(path, sep=",")
        if flat.size == 0:
            raise ValueError("empty fromfile result")
    except Exception:
        data = np.loadtxt(path, delimiter=",")
        flat = data.ravel()

    if flat.size % 2 != 0:
        raise ValueError(f"CSV {path} has unexpected number of elements {flat.size}")

    # If file is 2 x N (two rows: re row, im row) then total elements == 2*ncols
    if ncols > 0 and flat.size == 2 * ncols:
        data2 = flat.reshape(2, ncols)
        re = data2[0, :]
        im = data2[1, :]
    else:
        # interpret as interleaved pairs
        flat2 = flat.reshape(-1, 2)
        re = flat2[:, 0]
        im = flat2[:, 1]

    return re, im


def main():
    parser = argparse.ArgumentParser(description="Live constellation plot from CSV files")
    parser.add_argument("folder", nargs="?", default="../../../savannah_wesn/data",
                        help="Folder to watch for CSV files (default: ../../../savannah_wesn/data)")
    parser.add_argument("--interval", type=float, default=0.1,
                        help="Polling interval in seconds (default: 0.1)")
    parser.add_argument("--marker-size", type=float, default=5.0,
                        help="Marker size for scatter plot")
    args = parser.parse_args()

    folder = args.folder

    plt.ion()
    fig, ax = plt.subplots()
    sc = None

    last_path = None
    last_mtime = 0
    point_count = None

    try:
        while True:
            latest = get_latest_csv(folder)
            if latest is None:
                print(f"No CSV files found in {folder}. Waiting...")
                time.sleep(args.interval)
                continue

            try:
                mtime = os.path.getmtime(latest)
            except OSError:
                time.sleep(args.interval)
                continue

            # If file changed (or we switched to a new latest file), reload
            if latest != last_path or mtime != last_mtime:
                try:
                    re, im = load_iq_from_csv(latest)
                except Exception as e:
                    print(f"Failed to load '{latest}': {e}")
                    last_path = latest
                    last_mtime = mtime
                    time.sleep(args.interval)
                    continue
                xy = np.column_stack((re, im))

                # initialize scatter with fixed axes and point count
                if sc is None:
                    point_count = xy.shape[0]
                    sc = ax.scatter(xy[:, 0], xy[:, 1], s=args.marker_size, edgecolors='none')
                    ax.axhline(0, linewidth=0.5)
                    ax.axvline(0, linewidth=0.5)
                    ax.set_xlabel("In-phase (I)")
                    ax.set_ylabel("Quadrature (Q)")
                    ax.set_title("Constellation Diagram")
                    ax.set_aspect("equal", adjustable="box")
                    ax.grid(True)
                    # fix axes to the requested range for speed
                    ax.set_xlim(-1.5, 1.5)
                    ax.set_ylim(-1.5, 1.5)
                    ax.set_autoscale_on(False)
                else:
                    # if the incoming file has same number of points, update offsets
                    if xy.shape[0] == point_count:
                        sc.set_offsets(xy)
                    else:
                        # fallback: recreate scatter if sizes differ
                        point_count = xy.shape[0]
                        sc.remove()
                        sc = ax.scatter(xy[:, 0], xy[:, 1], s=args.marker_size, edgecolors='none')

                # draw once per file update
                fig.canvas.draw_idle()
                fig.canvas.flush_events()

                print(f"Loaded '{latest}' ({xy.shape[0]} points)")

                last_path = latest
                last_mtime = mtime

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("Exiting (KeyboardInterrupt)")
        plt.ioff()
        plt.show()


if __name__ == "__main__":
    main()