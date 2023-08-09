#!/bin/bash

################################################################################
# This script runs the Agora in simulation mode in one configurations.
# It accepts a specific config file (can be overwrite by argument) and run an
# instance of experiment.
#
# For easier debug and experiemnt, this script also accepts a set of parameters
# to put on the output filename. They are NOT related to the experiment config.
# Those param include:
#   - 5G Numerologies (0-3)
#   - Traffic load: num of U's
#   - Modulation scheme
#   - LDPC code rate
#   - Number of worker threads
#
# Copyright 2023 @cstandy
################################################################################


################################################################################
# Env and exe path setting
################################################################################
cur_dir=$(pwd)
agora_dir=/home/ct297/workspace/agora_single-core-sim/
build_dir=$agora_dir/build
exe=$build_dir/agora
user=$build_dir/sender
data_gen_exe=$build_dir/data_generator
# config=$agora_dir/files/config/ci/tddconfig-sim-ul.json
# config=$agora_dir/files/config/ci/tddconfig-sim-ul-fr2.json
config=$agora_dir/files/config/ci/tddconfig-sim-ul-fr2-autogen.json
logpath=$agora_dir/log

################################################################################
# Internal setting
################################################################################
mu=0
num_worker=0
num_uplink=3
code_rate="0p333"
modulation="16QAM"

################################################################################
# Override variable for command
################################################################################

# Function to display help
function display_help {
    echo "Usage: ./test_sim-ul.sh [option]"
    echo "Options:"
    echo "  -u, --mu               - numerology [0-3]"
    echo "  -w, --num_worker       - number of worker threads"
    echo "  --num_uplink           - number of uplink symbols [0-13]"
    echo "  -h, --help             - display this help message"
    echo "  --conf_file            - name of config file"
    echo "  --code_rate            - code rate"
    echo "  --modulation           - modulation scheme"
    echo "  --agora_dir            - absolute path to the directory of compiled Agora"
}

# Process command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        "-u" | "--mu")
            mu="$2"
            shift 2
            ;;
        "-w" | "--num_worker")
            num_worker="$2"
            shift 2
            ;;
        "--num_uplink")
            num_uplink="$2"
            shift 2
            ;;
        "--conf_file")
            config="$2"
            shift 2
            ;;
        "--code_rate")
            code_rate="$2"
            shift 2
            ;;
        "--modulation")
            modulation="$2"
            shift 2
            ;;
        "--agora_dir")
            agora_dir="$2"
            shift 2
            ;;
        "-h" | "--help")
            display_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

logfile=$logpath/$(date +"%Y-%m-%d_%H-%M-%S")_u${num_uplink}_cr${code_rate}_${modulation}_mu${mu}_w${num_worker}.log

################################################################################
# Print config
################################################################################

echo "--------------------------------------------------------------------------------"
echo "| Config                                                                       |"
echo "--------------------------------------------------------------------------------"
echo "[info] Agora dir: $agora_dir"
echo "[info] config file name: $config"
echo "[info] output file name: $logfile"
echo "--------------------------------------------------------------------------------"
echo "| Variables only for output file name                                          |"
echo "--------------------------------------------------------------------------------"
echo "[info] numerology = $mu"
echo "[info] number of worker threads = $num_worker"
echo "[info] number of uplink symbols = $num_uplink"
echo "[info] LDPC code rate = $code_rate"
echo "[info] modulation = $modulation"
echo "--------------------------------------------------------------------------------"

################################################################################
# Main Program
################################################################################

echo "[cmd] cd $agora_dir"
cd $agora_dir

echo "[info] Generating the data for simulation..."
echo "[cmd] $data_gen_exe --conf_file $config > $cur_dir/data_gen.log"
$data_gen_exe --conf_file $config > $cur_dir/data_gen.log

# Use timeout to avoid errorneous alignment between bs and ue
# use SIGINT to let Agora prints stat instead of SIGKILL with hard stop
echo "[info] Starting base station..."
echo "[cmd] $exe --conf_file $config > $logfile 2>&1 &"
$exe --conf_file $config > $logfile 2>&1 &
pid_bs=$!

sleep 3

echo "[info] Starting user equipment..."
echo "[cmd] $user --conf_file $config --num_threads=2 --core_offset=10 --enable_slow_start=0 > $cur_dir/sender.log & "
$user --conf_file $config   \
      --num_threads=2       \
      --core_offset=10      \
      --enable_slow_start=0 \
      > $cur_dir/sender.log &
pid_ue=$!

echo "[info] Simulating traffic..."

# wait for the sender to finish
wait $pid_ue

if ps -p $pid_bs > /dev/null; then
    echo "[warning] Base station not receiving all frames, sending SIGINT to stop simulation."
    kill -SIGINT $pid_bs
fi

echo "[info] All child processes have finished."
