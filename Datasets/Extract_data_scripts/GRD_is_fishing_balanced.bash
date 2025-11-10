for i in $(seq 1 187)
do
    sbatch GRD_is_fishing_balanced.slurm $i 
done
