#!/bin/bash

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m' # pink
CYAN='\033[0;36m'
LIGHTGRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
LIGHTRED='\033[1;31m'
LIGHTGREEN='\033[1;32m'
LIGHTYELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
LIGHTMAGENTA='\033[1;35m'
LIGHTCYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Print step with dynamic color
print_step() {
    local color=$1
    local message=$2
    echo -e "${color}----------------------------------------------------------------${NC}"
    echo -e "${color}${message}${NC}"
    echo -e "${color}----------------------------------------------------------------${NC}"
}

# Print sub-step with dynamic color
print_sub_step() {
    local color=$1
    local message=$2
    echo -e "${color}---- ${message} ----${NC}"
}

print_step $GREEN "Step 1: Check Environment"
bash check_env.sh
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All required libraries are installed.${NC}"
else
    exit 1
fi


print_step $YELLOW "Step 2: Prepare RL-Spatial Indices"
print_sub_step $GREEN "Step 2.1: Prepare BMTree"
sh rl_baseline/prepare_bmtree.sh

echo -e "${RED}If you have any environment related question in running Learned-BMTree, please check environment.yml under Learned-BMTree.${NC}"
echo -e "${GREEN}BMTree is installed.${NC}"

print_sub_step $YELLOW "Step 2.2: Prepare RLRtree"
print_sub_step $YELLOW "Step 2.3: Prepare Qd-tree"

export LD_LIBRARY_PATH=/home/liuguanli/Documents/libtorch/lib:$LD_LIBRARY_PATH

print_step $YELLOW "Step 3: Start Experiments"


python run_exp_from_config.py