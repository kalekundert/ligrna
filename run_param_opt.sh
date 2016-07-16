#!/usr/bin/env sh
set -euo pipefail

# Clean up old files
rm -rf stdout
mkdir -p stdout

# Submit the design jobs
fixed_args="inputs/mh_7.yml inputs/scorefxn.yml -n1000"

declare -A parameter_args
parameter_args[auto_25]="-T 'auto 25'"
parameter_args[auto_50]="-T 'auto 50'"
parameter_args[auto_75]="-T 'auto 75'"
parameter_args[anneal_T_1]="-T '1 to 0 in 500 steps'"
parameter_args[anneal_T_2]="-T '2 to 0 in 500 steps'"
parameter_args[anneal_T_4]="-T '4 to 0 in 500 steps'"

declare -A spacer_args
spacer_args[no_spacers]=''
spacer_args[example_spacers]='inputs/example_spacers.yml'
spacer_args[random_spacers]='inputs/random_spacers.yml'

for params in "${!parameter_args[@]}"; do
    for spacer in "${!spacer_args[@]}"; do
        output_dir="results/param_opt/${params}/${spacer}"
        rm -rf ${output_dir}; mkdir -p ${output_dir}
        qsub -t 1-10 -v "OUTPUT_PREFIX=${output_dir},ADDAPT_ARGS=${fixed_args} ${parameter_args[$params]} ${spacer_args[$spacer]}" sgrna_mc
    done
done
