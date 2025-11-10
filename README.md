# Extract-SARFish-Data

Welcome to the GitHub repository for the paper titled "Maritime object classification with SAR imagery using quantum kernel methods". This repository contains all the instructions and codes necessary to extract the SAR chip image datasets utilised in the paper from the SARFish dataset. Specifically, after downloading the SARFish dataset (instructions for which can be found in the links provided in [the paper for the SARFish dataset](https://openaccess.thecvf.com/content/WACV2024W/CDL/papers/Luckett_The_SARFish_Dataset_and_Challenge_WACVW_2024_paper.pdf)) in .zip format, the codes available in this repository can be used to unzip and extract large balanced datasets of 16x16 GRD, 16x16 SLC, and 70x12 SLC chip images. Using these large balanced datasets, we provide codes which then sample the exact balanced datasets which are utilised in our paper. Note though, that these codes are written to be exectued on HPC architecture with the Slurm Workload Manager. This requires the user to be permitted to submit at least 760 jobs to the queue at once.

We kindly request users who wish to use the datasets in their own research to cite both our paper and the original [the paper for the SARFish dataset](https://openaccess.thecvf.com/content/WACV2024W/CDL/papers/Luckett_The_SARFish_Dataset_and_Challenge_WACVW_2024_paper.pdf).

## Contents

- [Datasets](./Datasets):

  - [Unzip_data_scripts](./Datasets/Unzip_data_scripts):
 
    This folder contains scripts used to unzip the SARFish data files after they have been downloaded. 

  - [Extract_data_scripts](./Datasets/Extract_data_scripts):
 
    This folder contains scripts used to extract the large balanced datasets of SAR chip images, from which the datasets utilised in our paper are sampled.

- [Labels](./Labels):

  - [GRD_train.csv](./Labels/GRD_train), [GRD_validation.csv](./Labels/GRD_validation), [SLC_train.csv](./Labels/SLC_train), [SLC_validation.csv](./Labels/SLC_validation): 
 
    These `.csv` files come from the SARFish dataset and contain information about all of the detected objects in the SARFish data files that are unzipped by the scripts in the [Unzip_data_scripts](./Datasets/Unzip_data_scripts) folder.

  - [GRD_is_fishing_HIGH_confidence_balanced.csv](./Labels/GRD_is_fishing_HIGH_confidence_balanced.csv), [GRD_is_vessel_HIGH_confidence_balanced.csv](./Labels/GRD_is_vessel_HIGH_confidence_balanced.csv), [SLC_is_fishing_HIGH_confidence_balanced.csv](./Labels/SLC_is_fishing_HIGH_confidence_balanced.csv), [SLC_is_vessel_HIGH_confidence_balanced.csv](./Labels/SLC_is_vessel_HIGH_confidence_balanced.csv):
 
    These `.csv` files contain the rows of the [GRD_train.csv](./Labels/GRD_train), [GRD_validation.csv](./Labels/GRD_validation), [SLC_train.csv](./Labels/SLC_train), [SLC_validation.csv](./Labels/SLC_validation) files which relate to the subset of the detected objects used to construct the large balanced datasets of SAR chip images from which the datasets utilised in our paper are sampled.

- [Datasets](./Datasets):

  This folder contains extra results, including the accuracy, precision, recall, and F1-score's obtained on the false class of the training and testing datasets considered in our paper, together with the macro (and weighted, which for balanced datasets such as the ones we utilise are the same as the macro) averages of the reported metrics.

# Usage instructions

As a preliminary note, the `.slurm` files may require extra or fewer `#SBATCH` directives depending on the configuration of the HPC architecture being used to execute the scripts.

## Unzipping the SARFish data files

To unzip the SARFish data files, first `cd` into the [Unzip_data_scripts](./Datasets/Unzip_data_scripts) folder. The next step is then to edit the `Unzipper_GRD.bash` and `Unzipper_SLC.bash` files and define the variable `path_to_SARFish_dataset` to specify the path to the directory where the SARFish dataset has been downloaded. Note that the SARFish dataset contains a few terabytes of data. After this, by running the command:

```bash
bash Unzipper_GRD.bash
```

or

```bash
bash Unzipper_SLC.bash
```

from inside the [Unzip_data_scripts](./Datasets/Unzip_data_scripts) folder, a variety of Slurm jobs will be queued and all of the GRD or SLC data will be unzipped and stored in the [Datasets](./Datasets) folder.

## Extracting large balanced SAR chip image datasets from the SARFish dataset

The following commands will only work as intended once the scripts in the [Unzip_data_scripts](./Datasets/Unzip_data_scripts) folder have been used to unzip the data. Specifically, after the data has been unzipped, the first step is to `cd` into the [Extract_data_scripts](./Datasets/Extract_data_scripts) folder. Next, run the commands:
 
```bash
bash setup_GRD.bash
bash setup_SLC.bash
```

The above commands will set up some Python virtual environments that can load the unzipped GRD and SLC `.tiff` files. Note that the GRD `.tiff` files store data types `uint16`, while the SLC `.tiff` files store data types `Complex64`. For this reason we create two separate Python virtual environments, since the GRD files can be loaded with the Python package `PIL` (AKA `pillow`), but the SLC files required the Python package `tifffile`, since `PIL` doesn't work for `Complex64`. After setting up the Python virtual environments, the next step required to extract the 6 datasets used in the paper is to run the command:

```bash
bash <dataset>.bash
```

where `<dataset>` is replaced with one of `GRD_is_vessel_balanced`, `GRD_is_fishing_balanced`, `SLC_is_vessel_balanced`, or `SLC_is_fishing_balanced`. Note that, in their current form, the scripts for the SLC data will extract the 16x16 chips. To instead extract the 70x12 chips, we need to edit the files `SLC_is_vessel_balanced.py` and `SLC_is_fishing_balanced.py` and change the variables `image_width` and `image_height` to equal `70` and `12` respectively. We then need to change the hard coded filenames in the `Compile_SLC_is_fishing_balanced.py` and `Compile_SLC_is_vessel_balanced.py` files given by the `output_file` variable, replacing `16x16` with `70x12`. These changes only need to be made when extracting the 70x12 SLC datasets. After this the next step is to run the command:

```bash
sbatch Compile_<dataset>.slurm
```

where again `<dataset>` is replaced with one of `GRD_is_vessel_balanced`, `GRD_is_fishing_balanced`, `SLC_is_vessel_balanced`, or `SLC_is_fishing_balanced`. The two commands above will create one of the 6 large balanced datasets of SAR chip images from which the datasets utilised in our paper are sampled.

## Sampling the specific datasets used in the paper

Assuming you have completed all of the instructions above, the following codes can be used to import the specific datasets utilised in the paper. As you will see, the large balanced datasets constructed in the previous subsection contain more data than we used in our paper, however using more data requires more compute time, so we did not scale up the amount of data utilised in our paper. Similarly, the datasets contain both VH and VV polarised data, but we only used the VH polarised data in our work. Note that the following codes require the Python packages `scikit-learn`, `h5py`, and `numpy` to be installed. 

To import the datasets, we start by importing the necessary packages:

```python
# Import packages
import h5py
import numpy as np
from sklearn.utils import resample
```

Next we execute one of the following blocks of code depending on which dataset we want to import, replacing `<path_to_Datasets_folder>` with the path to the [Datasets](./Datasets) folder:

- To import the 16x16 GRD dataset used for the `is_vessel` task:

  ```python
  # Specify the file path to the .h5 dataset
  h5_file_path = '<path_to_Datasets_folder>/GRD_isVessel_7600samples_16x16patches_HIGHconfidence_balanced.h5'
  # Specify how many samples per class we should have (in training and testing together)
  num_samples_per_class = 625
  # Open the .h5 file and import the data
  with h5py.File(h5_file_path, 'r') as f:
      X_all = f['VH_dataset'][:]
      y_all = f['is_vessel'][:].astype(bool)
  ```

- To import the 16x16 GRD dataset used for the `is_fishing` task:

  ```python
  # Specify the file path to the .h5 dataset
  h5_file_path = '<path_to_Datasets_folder>/GRD_isFishing_1864samples_16x16patches_HIGHconfidence_balanced.h5'
  # Specify how many samples per class we should have (in training and testing together)
  num_samples_per_class = 625
  # Open the .h5 file and import the data
  with h5py.File(h5_file_path, 'r') as f:
      X_all = f['VH_dataset'][:]
      y_all = f['is_fishing'][:].astype(bool)
  ```

- To import the 16x16 SLC dataset used for the `is_vessel` task:

  ```python
  # Specify the file path to the .h5 dataset
  h5_file_path = '<path_to_Datasets_folder>/SLC_isVessel_7614samples_16x16patches_HIGHconfidence_balanced.h5'
  # Specify how many samples per class we should have (in training and testing together)
  num_samples_per_class = 625
  # Open the .h5 file and import the data
  with h5py.File(h5_file_path, 'r') as f:
      X_all = f['VH_dataset'][:]
      y_all = f['is_vessel'][:].astype(bool)
  ```

- To import the 16x16 SLC dataset used for the `is_fishing` task:

  ```python
  # Specify the file path to the .h5 dataset
  h5_file_path = '<path_to_Datasets_folder>/SLC_isFishing_1852samples_16x16patches_HIGHconfidence_balanced.h5'
  # Specify how many samples per class we should have (in training and testing together)
  num_samples_per_class = 625
  # Open the .h5 file and import the data
  with h5py.File(h5_file_path, 'r') as f:
      X_all = f['VH_dataset'][:]
      y_all = f['is_fishing'][:].astype(bool)
  ```

- To import the 70x12 SLC dataset used for the `is_vessel` task:

  ```python
  # Specify the file path to the .h5 dataset
  h5_file_path = '<path_to_Datasets_folder>/SLC_isVessel_7614samples_70x12patches_HIGHconfidence_balanced.h5'
  # Specify how many samples per class we should have (in training and testing together)
  num_samples_per_class = 625
  # Open the .h5 file and import the data
  with h5py.File(h5_file_path, 'r') as f:
      X_all = f['VH_dataset'][:]
      y_all = f['is_vessel'][:].astype(bool)
  ```

- To import the 70x12 SLC dataset used for the `is_fishing` task:

  ```python
  # Specify the file path to the .h5 dataset
  h5_file_path = '<path_to_Datasets_folder>/SLC_isFishing_1852samples_70x12patches_HIGHconfidence_balanced.h5'
  # Specify how many samples per class we should have (in training and testing together)
  num_samples_per_class = 625
  # Open the .h5 file and import the data
  with h5py.File(h5_file_path, 'r') as f:
      X_all = f['VH_dataset'][:]
      y_all = f['is_fishing'][:].astype(bool)
  ```

Finally, we sample the datasets used in our paper from the total datasets and define the variables `X_train`, `X_test`, `y_train`, and `y_test` to store the input training data, input testing data, training labels, and testing labels respectively using the following block of code:

```python
# Flatten the images into 256-dimensional feature vectors
X_all = X_all.reshape(X_all.shape[0], -1)
# Split by class
X_true = X_all[y_all]
X_false = X_all[~y_all]
# Sample balanced data
X_true_sampled = resample(X_true, n_samples=num_samples_per_class, random_state=42)
X_false_sampled = resample(X_false, n_samples=num_samples_per_class, random_state=42)
y_true_sampled = np.ones(num_samples_per_class)
y_false_sampled = np.zeros(num_samples_per_class)
# Combine the data
X_data = np.concatenate([X_true_sampled, X_false_sampled], axis=0)
y_data = np.concatenate([y_true_sampled, y_false_sampled], axis=0)
# Split into training and testing sets (80% training)
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=42, stratify=y_data)
```
