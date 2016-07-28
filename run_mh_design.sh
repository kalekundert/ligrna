#!/usr/bin/env sh
set -euo pipefail

# Submit the design jobs
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/mh_design/random_spacers/mh_6" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/mh_design/random_spacers/mh_7" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/mh_design/example_spacers/mh_6" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/mh_design/example_spacers/mh_7" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/mh_design/no_spacers/mh_6" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/mh_design/no_spacers/mh_7" sgrna_mc

#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/misfold_nexus/mh_6.yml -n10000 inputs/misfold_nexus/scorefxn.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/misfold_nexus/random_spacers/mh_6" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/misfold_nexus/mh_7.yml -n10000 inputs/misfold_nexus/scorefxn.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/misfold_nexus/random_spacers/mh_7" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/misfold_nexus/mh_6.yml -n10000 inputs/misfold_nexus/scorefxn.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/misfold_nexus/example_spacers/mh_6" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/misfold_nexus/mh_7.yml -n10000 inputs/misfold_nexus/scorefxn.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/misfold_nexus/example_spacers/mh_7" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/misfold_nexus/mh_6.yml -n10000 inputs/misfold_nexus/scorefxn.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/misfold_nexus/no_spacers/mh_6" sgrna_mc
#qsub -t 1-25 -v "ADDAPT_ARGS=inputs/misfold_nexus/mh_7.yml -n10000 inputs/misfold_nexus/scorefxn.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/misfold_nexus/no_spacers/mh_7" sgrna_mc

qsub -t 1-25 -v "ADDAPT_ARGS=inputs/in_vitro/mh_7.yml -n10000 inputs/theo_aptamer.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/in_vitro/random_spacers/mh_7" sgrna_mc
qsub -t 1-25 -v "ADDAPT_ARGS=inputs/in_vitro/mh_7.yml -n10000 inputs/theo_aptamer.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/in_vitro/example_spacers/mh_7" sgrna_mc
qsub -t 1-25 -v "ADDAPT_ARGS=inputs/in_vitro/mh_7.yml -n10000 inputs/theo_aptamer.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/in_vitro/no_spacers/mh_7" sgrna_mc
