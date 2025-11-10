VENV_NAME="PythonTifffileEnv"
if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv "$VENV_NAME"
    source "$VENV_NAME/bin/activate"
    pip install h5py
    pip install pandas
    pip install numpy
    pip install tifffile
else
    source "$VENV_NAME/bin/activate"
fi
