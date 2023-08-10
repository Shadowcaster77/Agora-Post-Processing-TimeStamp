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

echo "--------------------------------------------------------------------"
echo "#    # #    # #      ##### #        ####   ####  #####  ###### ";
echo "##  ## #    # #        #   #       #    # #    # #    # #      ";
echo "# ## # #    # #        #   # ##### #      #    # #    # #####  ";
echo "#    # #    # #        #   #       #      #    # #####  #      ";
echo "#    # #    # #        #   #       #    # #    # #   #  #      ";
echo "#    #  ####  ######   #   #        ####   ####  #    # ###### ";
echo "--------------------------------------------------------------------"

################################################################################
# Env and exe path setting
################################################################################
cur_dir=$(pwd)
agora_dir=/home/ct297/workspace/agora_origin/
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
num_worker=1
num_uplink=4
code_rate=0.333
modulation="16QAM"

################################################################################
# Override variable for command
################################################################################

# Function to display help
function display_help {
    echo "Usage: ./test_5g.sh [option]"
    echo "Options:"
    echo "  --num_uplink           - number of uplink symbols [0-13]"
    echo "  --conf_file            - name of config file"
    echo "  --code_rate            - code rate"
    echo "  --modulation           - modulation scheme"
    echo "  -h, --help             - display this help message"
}

# Process command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
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

code_rate_str="${code_rate//./p}"

################################################################################
# Print config
################################################################################

echo "--------------------------------------------------------------------"
echo "   ____     ____        __      _   _________    _____      _____   ";
echo "  / ___)   / __ \      /  \    / ) (_   _____)  (_   _)    / ___ \  ";
echo " / /      / /  \ \    / /\ \  / /    ) (___       | |     / /   \_) ";
echo "( (      ( ()  () )   ) ) ) ) ) )   (   ___)      | |    ( (  ____  ";
echo "( (      ( ()  () )  ( ( ( ( ( (     ) (          | |    ( ( (__  ) ";
echo " \ \___   \ \__/ /   / /  \ \/ /    (   )        _| |__   \ \__/ /  ";
echo "  \____)   \____/   (_/    \__/      \_/        /_____(    \____/   ";
echo "                                                                    ";
echo "--------------------------------------------------------------------"
echo "[info] Agora dir: $agora_dir"
echo "[info] number of uplink symbols = $num_uplink"
echo "[info] LDPC code rate = $code_rate"
echo "[info] modulation = $modulation"
echo "--------------------------------------------------------------------"
echo "[info] Iterate thru mu 0-3 and worker 1, 2, 4, 8, 16"
echo "[info] Please check if Agora is compiled"

################################################################################
# Confirm the config
################################################################################

read -p "Do you want to continue? (yes/no): " response

if [[ "$response" == "yes" ]]; then
    echo "Continuing..."
    # Add your commands here
else
    echo "Quitting..."
    exit 0
fi

echo "--------------------------------------------------------------------"

################################################################################
# Main Program
################################################################################

for num_worker in 1 2 4 8 16; do
    for mu in {0..3}; do

        echo "███╗   ██╗███████╗██╗    ██╗    ██████╗  ██████╗ ██╗   ██╗███╗   ██╗██████╗ ";
        echo "████╗  ██║██╔════╝██║    ██║    ██╔══██╗██╔═══██╗██║   ██║████╗  ██║██╔══██╗";
        echo "██╔██╗ ██║█████╗  ██║ █╗ ██║    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║██║  ██║";
        echo "██║╚██╗██║██╔══╝  ██║███╗██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║██║  ██║";
        echo "██║ ╚████║███████╗╚███╔███╔╝    ██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝";
        echo "╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ";
        echo "                                                                            ";

        echo "[info] Modifying JSON config"
        echo "pipenv run python $cur_dir/../python/update_config_json.py --mu $mu --num_uplink $num_uplink --num_worker $num_worker --code_rate $code_rate --modulation $modulation --agora_dir $agora_dir"
        pipenv run python $cur_dir/../python/update_config_json.py --mu $mu --num_uplink $num_uplink --num_worker $num_worker --code_rate $code_rate --modulation $modulation --agora_dir $agora_dir

        echo "[info] Calling Agora execution script"
        echo "$cur_dir/test_sim-ul.sh --mu $mu --num_uplink $num_uplink --num_worker $num_worker --code_rate $code_rate_str --modulation $modulation --agora_dir $agora_dir"
        $cur_dir/test_sim-ul.sh --mu $mu --num_uplink $num_uplink --num_worker $num_worker --code_rate $code_rate_str --modulation $modulation --agora_dir $agora_dir

    done
done