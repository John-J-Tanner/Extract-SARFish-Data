import os
import glob
import h5py
import numpy as np
import pandas as pd
from PIL import Image
import sys

i = int(sys.argv[1])

# Parameters
image_width = 16  # total width of the extracted patch
image_height = 16  # total height of the extracted patch
half_width = image_width // 2
half_height = image_height // 2

# Load CSV
csv_path = '../../Labels/GRD_is_fishing_HIGH_confidence_balanced.csv'
df = pd.read_csv(csv_path)[(i-1)*10:i*10]

# Make directory
if not os.path.exists('./GRD_uncompiled'):
    os.makedirs('./GRD_uncompiled')

# Disable decompression bomb check
Image.MAX_IMAGE_PIXELS = None

# Storage for patches and labels
vh_patches = []
vv_patches = []
labels = []

# Define the chunk extractor
def extract_chunk(image, middle_x, middle_y, num_x_direction, num_y_direction):
    width, height = image.size
    left = max(middle_x - num_x_direction, 0)
    right = min(middle_x + num_x_direction, width)
    top = max(middle_y - num_y_direction, 0) 
    bottom = min(middle_y + num_y_direction, height)
    cropped_image = image.crop((left, top, right, bottom))
    return np.array(cropped_image)

# Loop through each row
for _, row in df.iterrows():
    partition = row['partition']
    identifier = row['GRD_product_identifier']
    col = int(row['detect_scene_column'])
    row_idx = int(row['detect_scene_row'])
    label = bool(row['is_fishing'])

    base_path = os.path.join(
        '../GRD',
        partition,
        f'{identifier}.SAFE',
        'measurement'
    )

    # Load VH image
    vh_files = glob.glob(os.path.join(base_path, '*vh*.tiff'))
    vv_files = glob.glob(os.path.join(base_path, '*vv*.tiff'))
    if not vh_files or not vv_files:
        print(f"Skipping {identifier}: VH or VV .tiff not found")
        continue

    vh_image = Image.open(vh_files[0])
    vv_image = Image.open(vv_files[0])

    # Extract patches
    vh_patch = extract_chunk(vh_image, col, row_idx, half_width, half_height)
    vv_patch = extract_chunk(vv_image, col, row_idx, half_width, half_height)

    # Store
    vh_patches.append(vh_patch)
    vv_patches.append(vv_patch)
    labels.append(label)

# Save to HDF5
with h5py.File(f'./GRD_uncompiled/GRD_isFishing_1864samples_{image_width}x{image_height}patches_HIGHconfidence_balanced_batch{i:03d}.h5', 'w') as h5f:
    h5f.create_dataset('VH_dataset', data=np.array(vh_patches))
    h5f.create_dataset('VV_dataset', data=np.array(vv_patches))
    h5f.create_dataset('is_fishing', data=np.array(labels, dtype=bool))
