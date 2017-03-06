#!/bin/bash
#SBATCH -n 1                    # Number of cores
#SBATCH -N 1                    # Ensure that all cores are on one machine
#SBATCH -t 2-00:10              # Runtime in D-HH:MM
#SBATCH -p holyseasgpu          # Partition to submit to
#SBATCH --mem=30000               # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o log      # File to which STDOUT will be written
#SBATCH -e err      # File to which STDERR will be written

source activate NLP

for n in 100 1000 10000 100000
do
	for p in 10 100 1000
	do
		python main.py $n $p
	done
done