#!/bin/bash
#SBATCH -n 1                    # Number of cores
#SBATCH -N 1                    # Ensure that all cores are on one machine
#SBATCH -t 5-5:10              # Runtime in D-HH:MM
#SBATCH -p stats         # Partition to submit to
#SBATCH --mem=60000               # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o log/log_bench     # File to which STDOUT will be written
#SBATCH -e err/err_bench      # File to which STDERR will be written

module load python/2.7.11-fasrc01
source activate deepstat
#module load keras
#KERAS_BACKEND=tensorflow python -c "from keras import backend"

#THEANO_FLAGS=device=gpu,floatX=float32 python my_keras_script.py

for n in 100000 # 1000 10000
do
	for p in 100 1000 # 10
	do
		printf "Num. train : %d  ,  Data dim. : %d\n" $n $p
		python benchmark.py $n $p
	done
done