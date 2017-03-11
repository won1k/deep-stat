module load python/2.7.11-fasrc01
conda create -n deepstat --clone="$PYTHON_HOME"
source activate deepstat

pip install keras # auto install theano
pip install tensorflow