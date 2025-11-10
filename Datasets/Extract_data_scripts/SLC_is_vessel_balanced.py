import os
import sys
import glob
import h5py
import numpy as np
import pandas as pd
import tifffile as tiff

i = int(sys.argv[1])

# Parameters
image_width = 16
image_height = 16
half_width = image_width // 2
half_height = image_height // 2

# Load CSV
csv_path = '../../Labels/SLC_is_vessel_HIGH_confidence_balanced.csv'
df = pd.read_csv(csv_path)[(i-1)*10:i*10]

# Make directory
if not os.path.exists('./SLC_uncompiled'):
    os.makedirs('./SLC_uncompiled')

# Storage for patches and labels
vh_patches = []
vv_patches = []
labels = []

# Define the chunk extractor
def extract_chunk(array, middle_x, middle_y, half_w, half_h):
    height, width = array.shape
    top = max(middle_y - half_h, 0)
    bottom = min(middle_y + half_h, height)
    left = max(middle_x - half_w, 0)
    right = min(middle_x + half_w, width)
    return array[top:bottom, left:right]

# Loop through each row
for _, row in df.iterrows():
    partition = row['partition']
    identifier = row['SLC_product_identifier']
    col = int(row['detect_scene_column'])
    row_idx = int(row['detect_scene_row'])
    label = bool(row['is_vessel'])
    swath = int(row['swath_index'])

    base_path = os.path.join(
        '../SLC',
        partition,
        f'{identifier}.SAFE',
        'measurement'
    )

    # Load VH and VV image files using tifffile
    vh_files = glob.glob(os.path.join(base_path, f'*iw{swath}*vh*.tiff'))
    vv_files = glob.glob(os.path.join(base_path, f'*iw{swath}*vv*.tiff'))
    if not vh_files or not vv_files:
        print(f"Skipping {identifier}: VH or VV .tiff not found")
        continue

    try:
        vh_array = tiff.imread(vh_files[0])
        vv_array = tiff.imread(vv_files[0])
    except Exception as e:
        print(f"Skipping {identifier} due to read error: {e}")
        continue

    # Extract complex-valued patches
    vh_patch = extract_chunk(vh_array, col, row_idx, half_width, half_height)
    vv_patch = extract_chunk(vv_array, col, row_idx, half_width, half_height)

    # Store
    vh_patches.append(vh_patch)
    vv_patches.append(vv_patch)
    labels.append(label)

# Save to HDF5
with h5py.File(f'./SLC_uncompiled/SLC_isVessel_7614samples_{image_width}x{image_height}patches_HIGHconfidence_balanced_batch{i:03d}.h5', 'w') as h5f:
    h5f.create_dataset('VH_dataset', data=np.array(vh_patches))
    h5f.create_dataset('VV_dataset', data=np.array(vv_patches))
    h5f.create_dataset('is_vessel', data=np.array(labels, dtype=bool))
