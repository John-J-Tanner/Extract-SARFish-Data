import h5py
import numpy as np
import os
import glob

# Directory containing the batch files
input_dir = './GRD_uncompiled'
output_file = '../GRD_isVessel_7600samples_16x16patches_HIGHconfidence_balanced.h5'

# Get sorted list of batch files
batch_files = sorted(glob.glob(os.path.join(input_dir, 'GRD_isVessel_7600samples_16x16patches_HIGHconfidence_balanced_batch*.h5')))

# Initialize lists to collect data
vh_data = []
vv_data = []
labels = []

# Load and append datasets
for file_path in batch_files:
    print(f"Reading {file_path}")
    with h5py.File(file_path, 'r') as f:
        vh_data.append(f['VH_dataset'][:])
        vv_data.append(f['VV_dataset'][:])
        labels.append(f['is_vessel'][:])

# Concatenate all data
vh_all = np.concatenate(vh_data, axis=0)
vv_all = np.concatenate(vv_data, axis=0)
labels_all = np.concatenate(labels, axis=0)

# Write to new HDF5 file
with h5py.File(output_file, 'w') as f_out:
    f_out.create_dataset('VH_dataset', data=vh_all, compression='gzip')
    f_out.create_dataset('VV_dataset', data=vv_all, compression='gzip')
    f_out.create_dataset('is_vessel', data=labels_all, compression='gzip')
