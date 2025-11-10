for i in $(seq 1 762)
do
    sbatch SLC_is_vessel_balanced.slurm $i
done
