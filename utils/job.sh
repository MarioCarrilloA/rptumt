#!/bin/bash
#SBATCH --gres=gpu:V100:1 # select a host with a Volta GPU
#SBATCH -t 30

rhrk-singularity pytorch_22.10-py3.simg --bind $(pwd):/mnt pwd
