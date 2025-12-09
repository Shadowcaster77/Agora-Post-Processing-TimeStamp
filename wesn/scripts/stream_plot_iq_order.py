import argparse
import glob
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import re
import itertools


def get_latest_csv(folder):
    pattern = os.path.join(folder, "*.csv")
    files = glob.glob(pattern)
    if not files:
        return None
    latest = max(files, key=os.path.getmtime)
    return latest


def parse_wesn_filename(name):
    """Parse filenames like wesn_output_frame_{frame}_sym_{sym}_ant_{ant}.csv
    Returns tuple (frame, sym, ant) or None if not matching.
    """
    m = re.search(r"wesn_output_frame_(\d+)_sym_(\d+)_ant_(\d+)\.csv$", name)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def list_ordered_files(folder):
    """Return dict mapping (frame,sym,ant) -> path for CSVs found in folder."""
    files = {}
    try:
        with os.scandir(folder) as it:
            for entry in it:
                if not entry.is_file():
                    continue
                if not entry.name.lower().endswith('.csv'):
                    continue
                parsed = parse_wesn_filename(entry.name)
                if parsed is None:
                    continue
                files[parsed] = entry.path
    except FileNotFoundError:
        return {}
    return files


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
        # use fromstring on the full file contents to avoid np.fromfile text warnings
        with open(path, "r") as f:
            content = f.read()
        flat = np.fromstring(content, sep=",")
        if flat.size == 0:
            raise ValueError("empty fromstring result")
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
    parser.add_argument("--interval", type=float, default=0.5,
                        help="Polling interval in seconds (default: 0.5)")
    parser.add_argument("--marker-size", type=float, default=5.0,
                        help="Marker size for scatter plot")
    parser.add_argument("--update-pause", type=float, default=0.2,
                        help="Pause in seconds after updating each file for smoother demo (default: 0.2)")
    args = parser.parse_args()

    folder = args.folder

    import matplotlib
    backend = matplotlib.get_backend().lower()
    interactive_backend = any(s in backend for s in ("tk", "qt", "wx", "gtk", "macosx", "cocoa"))

    if interactive_backend:
        plt.ion()
    else:
        # non-interactive backends won't show a GUI; keep interactive calls harmless
        plt.ioff()
    fig, ax = plt.subplots()
    sc0 = None
    sc1 = None

    last_path = None
    last_mtime = 0
    point_count0 = None
    point_count1 = None
    last_seen = None  # tuple (frame,sym,ant) of last processed
    # reuse blit vars
    use_blit = False
    background = None

    try:
        # sequentially iterate frames and symbols and plot when file becomes available
        start_frame = getattr(args, 'start_frame', 0)
        start_sym = getattr(args, 'start_sym', 0)
        max_sym = getattr(args, 'max_sym', 10)
        ant = getattr(args, 'ant', 0)

        for frame in itertools.count(start=start_frame):
            for sym in range(start_sym if frame == start_frame else 0, max_sym + 1):
                # primary antenna (we wait for this), and secondary antenna (1) to plot in red if present
                primary_ant = ant
                secondary_ant = 1 if ant == 0 else 0

                filename0 = f"wesn_output_frame_{frame}_sym_{sym}_ant_{primary_ant}.csv"
                path0 = os.path.join(folder, filename0)
                filename1 = f"wesn_output_frame_{frame}_sym_{sym}_ant_{secondary_ant}.csv"
                path1 = os.path.join(folder, filename1)

                # wait until primary file exists; allow GUI events during wait
                while not os.path.exists(path0):
                    if interactive_backend:
                        plt.pause(args.interval)
                    else:
                        time.sleep(args.interval)

                # load primary
                try:
                    re0, im0 = load_iq_from_csv(path0)
                except Exception as e:
                    print(f"Failed to load '{path0}': {e}")
                    continue
                xy0 = np.column_stack((re0, im0))

                # try to load secondary if available (do not wait)
                xy1 = None
                if os.path.exists(path1):
                    try:
                        re1, im1 = load_iq_from_csv(path1)
                        xy1 = np.column_stack((re1, im1))
                    except Exception as e:
                        print(f"Failed to load secondary '{path1}': {e}")
                        xy1 = None

                # initialize artists if needed
                if sc0 is None:
                    point_count0 = xy0.shape[0]
                    sc0 = ax.scatter(xy0[:, 0], xy0[:, 1], s=args.marker_size, edgecolors='none', label=f'ant{primary_ant}')
                    if xy1 is not None:
                        point_count1 = xy1.shape[0]
                        sc1 = ax.scatter(xy1[:, 0], xy1[:, 1], s=args.marker_size, edgecolors='none', color='red', label=f'ant{secondary_ant}')
                    ax.axhline(0, linewidth=0.5)
                    ax.axvline(0, linewidth=0.5)
                    ax.set_xlabel("In-phase (I)")
                    ax.set_ylabel("Quadrature (Q)")
                    ax.set_title("Constellation Diagram")
                    ax.set_aspect("equal", adjustable="box")
                    ax.grid(True)
                    ax.set_xlim(-1.5, 1.5)
                    ax.set_ylim(-1.5, 1.5)
                    ax.set_autoscale_on(False)
                    try:
                        fig.canvas.draw()
                        background = fig.canvas.copy_from_bbox(ax.bbox)
                        use_blit = hasattr(fig.canvas, 'blit') and callable(fig.canvas.blit)
                    except Exception:
                        background = None
                        use_blit = False
                else:
                    # update primary
                    if xy0.shape[0] == point_count0:
                        sc0.set_offsets(xy0)
                    else:
                        point_count0 = xy0.shape[0]
                        sc0.remove()
                        sc0 = ax.scatter(xy0[:, 0], xy0[:, 1], s=args.marker_size, edgecolors='none', label=f'ant{primary_ant}')
                    # update secondary
                    if xy1 is not None:
                        if sc1 is None:
                            point_count1 = xy1.shape[0]
                            sc1 = ax.scatter(xy1[:, 0], xy1[:, 1], s=args.marker_size, edgecolors='none', color='red', label=f'ant{secondary_ant}')
                        else:
                            if xy1.shape[0] == point_count1:
                                sc1.set_offsets(xy1)
                            else:
                                point_count1 = xy1.shape[0]
                                sc1.remove()
                                sc1 = ax.scatter(xy1[:, 0], xy1[:, 1], s=args.marker_size, edgecolors='none', color='red', label=f'ant{secondary_ant}')

                # draw both artists
                if use_blit and background is not None:
                    try:
                        fig.canvas.restore_region(background)
                        ax.draw_artist(sc0)
                        if sc1 is not None:
                            ax.draw_artist(sc1)
                        fig.canvas.blit(ax.bbox)
                    except Exception:
                        fig.canvas.draw_idle()
                        fig.canvas.flush_events()
                else:
                    fig.canvas.draw_idle()
                    fig.canvas.flush_events()

                # pause briefly to make demo smoother (allow GUI events)
                upd_pause = getattr(args, 'update_pause', 0.2)
                if upd_pause and upd_pause > 0:
                    if interactive_backend:
                        plt.pause(upd_pause)
                    else:
                        time.sleep(upd_pause)

                print(f"Loaded primary '{path0}' frame={frame} sym={sym} ({xy0.shape[0]} points)" + (f" and secondary '{path1}' ({xy1.shape[0]} points)" if xy1 is not None else ""))

                # after first iteration, start_sym should be 0
                start_sym = 0

    except KeyboardInterrupt:
        print("Exiting (KeyboardInterrupt)")
        plt.ioff()
        # Show final window only for interactive backends, otherwise save image
        if interactive_backend:
            try:
                plt.show()
            except Exception:
                pass
        else:
            out = os.path.join(os.getcwd(), "last_constellation_order.png")
            try:
                plt.savefig(out, bbox_inches='tight', dpi=150)
                print(f"Saved last plot to {out}")
            except Exception as e:
                print(f"Could not save final plot: {e}")


if __name__ == "__main__":
    main()