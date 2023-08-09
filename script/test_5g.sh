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
# Iteration setting
################################################################################
mu=0
num_worker=0
config_idx=0

logfile=$logpath/$(date +"%Y-%m-%d_%H-%M-%S").log
timeout_duration=20

################################################################################
# Main Program
################################################################################

echo "[cmd] cd $agora_dir"
cd $agora_dir

echo " . Generating the data for simulation..."
echo "[cmd] $data_gen_exe --conf_file $config > $cur_dir/data_gen.log"
$data_gen_exe --conf_file $config > $cur_dir/data_gen.log
pid_datagen=$!

# Use timeout to avoid errorneous alignment between bs and ue
# use SIGINT to let Agora prints stat instead of SIGKILL with hard stop
echo " . Starting base station..."
echo "[cmd] timeout --signal=SIGINT $timeout_duration $exe --conf_file $config > $logfile 2>&1 &"
timeout --signal=SIGINT $timeout_duration $exe --conf_file $config > $logfile 2>&1 &
pid_bs=$!

sleep 5

echo " . Starting user equipment..."
echo "[cmd] $user --conf_file $config --num_threads=2 --core_offset=10 --enable_slow_start=0 > $cur_dir/sender.log & "
$user --conf_file $config   \
      --num_threads=2       \
      --core_offset=10      \
      --enable_slow_start=0 \
      > $cur_dir/sender.log &
pid_ue=$!

echo " . Simulating traffic..."

# wait for all background process to finish
wait

echo " . All child processes have finished."
