path_to_SARFish_dataset=<path_to_directory_containing_SARFish_dataset>

for file in ${path_to_SARFish_dataset}/sarfish/SARFishData/SLC/train/*
do
    sbatch Unzipper_SLC.slurm $file
done

for file in ${path_to_SARFish_dataset}/sarfish/SARFishData/SLC/validation/*
do
    sbatch Unzipper_SLC.slurm $file
done
