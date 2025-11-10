#!/bin/bash
#SBATCH --partition=work
#SBATCH --export=NONE
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=./OutFiles/SLC_is_fishing_balanced_%j.out
#SBATCH --exclusive

source setup_SLC.bash

time srun -N 1 -n 1 -c 1 python3 -u ./SLC_is_fishing_balanced.py $1
