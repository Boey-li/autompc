#!/bin/bash

###############################################################################
#
#SBATCH --time=160:00:00                  # Job run time (hh:mm:ss)
#SBATCH --nodes=1                        # Number of nodes
#SBATCH --ntasks-per-node=16             # Number of task (cores/ppn) per node
#SBATCH --job-name=grav_hopper      # Name of batch job
#SBATCH --partition=cs                   # Partition (queue)
#SBATCH --output=sbatch_out_2/grav_hopper.o%j           # Name of batch job output file
##SBATCH --error=sbatch_out_2/grav_hopper.e%j           # Name of batch job error file
#
###############################################################################

# Initialize Python environment 
module load anaconda/3
# module load openmpi
export CUDA_VISIBLE_DEVICES=
export OMP_NUM_THREADS=1

# Run job
# mpiexec -np 16 /home/baoyul2/.conda/envs/autompc/bin/python /home/baoyul2/autompc/autompc/model_metalearning/get_portfolio_configurations.py
/home/baoyul2/.conda/envs/autompc2/bin/python /home/baoyul2/autompc/autompc/model_metalearning/configurations_experiment/get_portfolio_configurations_14.py