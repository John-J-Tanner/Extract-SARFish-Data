#!/bin/bash
#SBATCH --partition=work
#SBATCH --export=NONE
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --output=./OutFiles/Unzipper_GRD_%j.out
#SBATCH --mem=10000MB

time srun -N 1 -n 1 -c 1 unzip $1 -d ../
