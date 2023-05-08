#!/bin/bash

#SBATCH --gres=gpu:V100:1
#SBATCH -o results-VGG16-%j.out
#SBATCH -e results-VGG16-%j.err
#SBATCH -t 08:00:00
#SBATCH --mem=32000

#Interactive
singularity run --nv --bind $(pwd):${HOME} /archive/singularity/tensorflow_23.01-tf2-py3.simg bash job.sh
