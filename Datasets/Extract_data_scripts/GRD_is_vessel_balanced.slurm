#!/bin/bash
#SBATCH --partition=work
#SBATCH --export=NONE
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --output=./OutFiles/GRD_is_vessel_balanced_%j.out
#SBATCH --mem=10000MB

source setup_GRD.bash

time srun -N 1 -n 1 -c 1 python3 -u ./GRD_is_vessel_balanced.py $1
