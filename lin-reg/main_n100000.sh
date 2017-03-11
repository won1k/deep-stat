#!/bin/bash
#SBATCH -n 1                    # Number of cores
#SBATCH -N 1                    # Ensure that all cores are on one machine
#SBATCH -t 5-00:10              # Runtime in D-HH:MM
#SBATCH -p unrestricted          # Partition to submit to
#SBATCH --mem=50000               # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o log/log_n100000      # File to which STDOUT will be written
#SBATCH -e err/err_n100000      # File to which STDERR will be written

source activate deepstat
#module load keras
#KERAS_BACKEND=tensorflow python -c "from keras import backend"

#THEANO_FLAGS=device=gpu,floatX=float32 python my_keras_script.py

for n in 100000
do
	for p in 10 100 1000
	do
		printf "Num. train : %d  ,  Data dim. : %d\n" $n $p
		python main.py $n $p
	done
done