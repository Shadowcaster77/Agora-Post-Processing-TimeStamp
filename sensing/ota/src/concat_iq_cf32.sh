#!/usr/bin/env bash
set -euo pipefail

# Concatenate multiple cf32 files (complex64 raw) into one file.
#
# Edit the FILES array below to include the cf32 files you want concatenated.
# You can also pass --out or -o on the command line to override the output filename.
#
# Example:
#   # edit FILES at top of this script, then:
#   ./concat_iq.sh
#   ./concat_iq.sh --out /tmp/combined.cf32


#############################################
# --- Edit this list to point at your cf32 files ---
FILES=(
  "../data/aux/silence100000.cf32"
  "../data/aux/zc8191.cf32"
  "../data/aux/guard5000.cf32"
  # "../data/rfsynth/ota_dense_ds3.32cf"
  # "../data/rfsynth/ota_dense.32cf"
  "../data/rfsynth/ota_sparse.32cf"
  # "../data/rfsynth/ota_std.32cf"
  # "../data/rfsynth/ota_test.32cf"
  "../data/aux/silence100000.cf32"
)
# --------------------------------------------------


# |<- silence ->|<---- ZC ---->|<- guard ->|<-- payload -->|<-- silence -->|
# |    1 ms     | 8191 samples | 5000 samp |    10.24 ms   |     1 ms      |

# assuming 100 MHz sampling rate:
# - 1 ms = 100k samples
# - 10.24 ms = 1024k samples
# - 8191 samples = 81.91 us


usage() {
  cat <<-USAGE
Usage: $0 [<outpath>]

This script concatenates cf32 files listed in the FILES array (edit the array at the top).
If <outpath> is not provided, the default output filename is concat_<nfiles>_<totalsamples>.cf32
Each complex sample is assumed to be 8 bytes (float32 I + float32 Q).
USAGE
}


OUT_OVERRIDE="${1:-}"
if [ "${OUT_OVERRIDE:-}" = "-h" ] || [ "${OUT_OVERRIDE:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ ${#FILES[@]} -eq 0 ]; then
  echo "No files listed in FILES. Edit the FILES array near the top of this script." >&2
  exit 2
fi

total_samples=0
declare -a file_samples

for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "Error: file not found: $f" >&2
    exit 3
  fi
  # get size in bytes (portable on linux stat -c%s)
  if ! bytes=$(stat -c%s -- "$f" 2>/dev/null); then
    # try BSD stat fallback
    bytes=$(stat -f%z -- "$f" 2>/dev/null || true)
  fi
  if [ -z "$bytes" ]; then
    echo "Unable to determine file size for $f" >&2
    exit 4
  fi

  # compute samples (each complex64 sample is 8 bytes)
  samples=$((bytes / 8))
  if [ $((bytes % 8)) -ne 0 ]; then
    echo "Error: file $f size ($bytes) is not divisible by 8 bytes (not an integral number of complex64 samples)" >&2
    exit 5
  fi
  file_samples+=("$samples")
  total_samples=$((total_samples + samples))
  echo "Read $samples samples ($bytes bytes) from $f"
done

nfiles=${#FILES[@]}

if [ -n "$OUT_OVERRIDE" ]; then
  out_path="$OUT_OVERRIDE"
  # if override is a directory, create default name inside
  if [ -d "$out_path" ] || [[ "$out_path" == */ ]]; then
    out_path="$out_path/concat_${nfiles}_${total_samples}.cf32"
  else
    out_dir=$(dirname -- "$out_path")
    if [ -n "$out_dir" ] && [ ! -d "$out_dir" ]; then
      mkdir -p "$out_dir"
    fi
  fi
else
  out_path="concat_${nfiles}_${total_samples}.cf32"
fi

echo "Writing ${total_samples} samples to ${out_path}"

# Concatenate files in order using a loop to avoid argument list limits
: > "$out_path"
for f in "${FILES[@]}"; do
  cat -- "$f" >> "$out_path"
done

echo "Wrote ${total_samples} samples to ${out_path}"

exit 0
