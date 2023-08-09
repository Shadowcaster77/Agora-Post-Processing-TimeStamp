#!/bin/bash

################################################################################
# This script runs the Agora in simulation mode in multiple configurations.
# The motivation is because 5G has multiple numerology, which has same workload
# but different time requirement.
# In this case, we often need to perform similar experiments to understand the
# system performance.
#
# Layer of iteration:
#
# - Traffic config: Traffic load & MCS (4 configs)
#     - Number of cores: single-core (0) vs. multi-cores (1, 2, 4, 8, 16)
#         - 5G Numerologies (0-3)
#
# - Traffic load: num of U's
# - MCS: modulation scheme and LDPC code rate
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
config=$agora_dir/files/config/ci/tddconfig-sim-ul-fr2.json
logpath=$agora_dir/log

################################################################################
# Internal setting
################################################################################
mu=0
num_worker=0
config_idx=0
timeout_duration=20

################################################################################
# Override variable for command
################################################################################

# Function to display help
function display_help {
    echo "Usage: ./test_5g.sh [option]"
    echo "Options:"
    echo "  -u, --mu               - numerology [0-3]"
    echo "  -w, --num_worker       - number of worker threads"
    echo "  -c, --config_idx       - config index [0-3]"
    echo "  -h, --help             - display this help message"
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
        "-c" | "--config_idx")
            config_idx="$2"
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

logfile=$logpath/$(date +"%Y-%m-%d_%H-%M-%S")_config-${config_idx}_mu${mu}_w${num_worker}.log

################################################################################
# Print config
################################################################################

echo "--------------------------------------------------------------------------------"
echo "| Config                                                                       |"
echo "--------------------------------------------------------------------------------"
echo "[info] config file name: $config"
echo "[info] config index = $config_idx"
echo "[info] output file name: $logfile"
echo "[info] numerology = $mu"
echo "[info] number of worker threads = $num_worker"
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
