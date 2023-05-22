#!/bin/bash

#SBATCH --gres=gpu:V100:1
#SBATCH -o results-yolov5-%j.out
#SBATCH -e results-yolov5-%j.err
#SBATCH -t 08:00:00
#SBATCH --mem=32000

singularity run --nv --bind $(pwd):$HOME /archive/singularity/pytorch_22.09-py3.simg bash job.sh
