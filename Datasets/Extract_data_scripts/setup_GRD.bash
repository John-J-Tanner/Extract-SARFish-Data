VENV_NAME="PythonPILEnv"
if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv "$VENV_NAME"
    source "$VENV_NAME/bin/activate"
    pip install h5py
    pip install pandas
    pip install numpy
    pip install pillow
else
    source "$VENV_NAME/bin/activate"
fi
