# OTA Experiments

This folder contains small utilities to prepare OTA transmit files (raw interleaved complex32, a.k.a. `cf32` / `numpy` `complex64`) from components (Zadoff–Chu preambles, silence/guard blocks, and payload samples).

### Directory Layout
- `src/`: scripts to generate building blocks and concatenate them.
	- [src/gen_zc.py](src/gen_zc.py): generate Zadoff–Chu sequences (cf32).
	- [src/gen_silence.py](src/gen_silence.py): generate complex-zero blocks (cf32).
	- [src/concat_iq_cf32.sh](src/concat_iq_cf32.sh): concatenate cf32 files listed in the script.
	- [src/helper/plot_zc.py](src/helper/plot_zc.py): plot I/Q, constellation and correlation with a ZC reference.
- `data/rfsynth/`: place or copy OTA sample payloads here (OTA recordings / synthesized payloads).
- `data/aux/`: intermediate building blocks (ZC, guard, silence) produced by `src/` scripts.
- `data/tx/`: final concatenated transmit files (created by `concat_iq_cf32.sh`).

### Prerequisites
- Use the Python environment in the parent repo.

## Overview of the workflow
1. Obtain or copy OTA payload samples into `data/rfsynth/`.
2. Generate Zadoff–Chu preambles and silence/guard blocks with the Python scripts under `src/` and dump them into `data/aux/`.
3. (Optional) Use `src/helper/plot_zc.py` to inspect the generated ZC sequence file.
4. Use `src/concat_iq_cf32.sh` to combine the ordered blocks into a single cf32 file and save it under `data/tx/`.

### Step-by-step usage

**1) Place payload OTA samples**
- Copy or generate payload(s) into `data/rfsynth/`. Example filenames used in the scripts are shown under `data/rfsynth/`.

**2) Generate ZC sequences**
- Generate a ZC sequence with length `N` and integer `root` (root must be coprime with `N`):

	```bash
	# create ZC length 8191
	python3 src/gen_zc.py --length 8191 --root 1 --out data/aux/zc8191.cf32
	```

	- `--length/-N` : sequence length (required)
	- `--root/-r` : integer root (default 1)
	- `--out/-o` : output file (raw cf32). If omitted, sequence is printed with `--print`.

**3) Generate silence/guard blocks**
- Create a block of complex zeros (useful for pre/post silence or guards):

	```bash
	# generates data/aux/silence100000.cf32 by default
	python3 src/gen_silence.py --length 100000 --out data/aux/
	```

	- `--length/-N` : number of complex samples (required)
	- `--out/-o` : output filename or directory (optional). When omitted the default filename is `silence<length>.cf32` in the current directory. When a directory is provided the file `silence<length>.cf32` is created in that directory. If a filename is provided it is used as-is.

**4) Concatenate components into a transmit file**
- Edit the array near the top of `src/concat_iq_cf32.sh` to list the component files (paths relative to the `sensing/ota` directory are used in the example):

	```bash
	# inside src/concat_iq_cf32.sh (FILES array)
	FILES=(
		"../data/aux/silence100000.cf32"
		"../data/aux/zc8191.cf32"
		"../data/aux/guard5000.cf32"
		"../data/rfsynth/ota_payload.cf32"
		"../data/aux/silence100000.cf32"
	)
	```

- Run the script (optional positional argument = output path). If you supply a directory it will create a default file named `concat_<nfiles>_<totalsamples>.cf32` inside that directory; otherwise pass a filename.

	```bash
	# specify output file (recommend to save under data/tx)
	./src/concat_iq_cf32.sh data/tx/ota_tx.cf32
	```

Notes:
- The script expects each input file to contain raw interleaved complex32 samples (I,Q float32) — i.e. `numpy.complex64` bytes. Each complex sample is 8 bytes; the script verifies file sizes are divisible by 8 and will error if not.
- Default output filename when not supplied: `concat_<nfiles>_<totalsamples>.cf32`.

**5) Inspect the result (optional)**
- Use the plot helper to visualize I/Q traces, constellation and correlation with a ZC reference:

	```bash
	python3 src/helper/plot_zc.py --file data/tx/ota_tx.cf32 --length 8191 --root 1 --outdir fig/
	```

	Output: three PNGs will be saved into the `--outdir` directory, prefixed by the input filename.

#### Troubleshooting & tips
- Confirm payload/sample files in `data/rfsynth/` are raw complex32 (no headers). You can inspect their size with `stat -c%s file` and check divisibility by 8.
- If you prefer to script the pipeline, the three main steps can be chained: generate ZC and silence into `data/aux/`, edit `src/concat_iq_cf32.sh` to point to files under `data/aux` and `data/rfsynth`, then run the concatenation script to produce `data/tx/`.

#### Files referenced
- [src/gen_zc.py](src/gen_zc.py)
- [src/gen_silence.py](src/gen_silence.py)
- [src/concat_iq_cf32.sh](src/concat_iq_cf32.sh)
- [src/helper/plot_zc.py](src/helper/plot_zc.py)

If you'd like, I can also add small wrapper examples that automate the whole flow (generate blocks then concatenate), or run a quick end-to-end test using generated files.
