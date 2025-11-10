path_to_SARFish_dataset=<path_to_directory_containing_SARFish_dataset>

for file in ${path_to_SARFish_dataset}/sarfish/SARFishData/GRD/train/*
do
    sbatch Unzipper_GRD.slurm $file
done

for file in ${path_to_SARFish_dataset}/sarfish/SARFishData/GRD/validation/*
do
    sbatch Unzipper_GRD.slurm $file
done
