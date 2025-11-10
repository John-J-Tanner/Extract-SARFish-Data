for i in $(seq 1 760)
do
    sbatch GRD_is_vessel_balanced.slurm $i
done
