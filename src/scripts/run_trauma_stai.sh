#!/bin/bash -l
#SBATCH -o ./logs/%A.out
#SBATCH -e ./logs/%A.err
#SBATCH --job-name=run_trauma_stai
#SBATCH --mail-type=ALL
#SBATCH --mail-user=akshaykjagadish@gmail.com
#SBATCH --time=72:00:00
#SBATCH --cpus-per-task=18


cd ~/gpt-trauma-induction/src

module purge
module load anaconda/3/2021.11
pip3 install --user openai ipdb python-dotenv tqdm
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

# run 3
python query.py --llm gpt4 --condition stai --prompt-length brief --seed 123 --proc-id 3 --num-runs 5
python query.py --llm gpt4 --condition trauma_stai --prompt-length brief --seed 123 --proc-id 3 --num-runs 5
python query.py --llm gpt4 --condition trauma_relaxation_stai --prompt-length brief --seed 123 --proc-id 3
python query.py --llm gpt4 --condition relaxation_stai --prompt-length brief --seed 123 --proc-id 3
python query.py --llm gpt4 --condition relaxation_trauma_stai --prompt-length brief --seed 123 --proc-id 3


