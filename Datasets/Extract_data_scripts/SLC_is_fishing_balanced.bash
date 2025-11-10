for i in $(seq 1 186)
do
    sbatch SLC_is_fishing_balanced.slurm $i
done
