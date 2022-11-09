#!/bin/bash

#SBATCH --job-name=run1D_testsuite
#SBATCH --account=e3sm
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=1Dtestsuite_all.out
#SBATCH --error=1Dtestsuite_all.error
#SBATCH --mail-user=njeffery@lanl.gov
#SBATCH --mail-type=ALL
#SBATCH --time=00:10:00

# Sample job script for chrysalis
# Run with
# > sbatch ./job_script.sh

source /lcrc/soft/climate/compass/chrysalis/load_latest_compass_gnu_openmpi.sh
source /lcrc/soft/climate/e3sm-unified/load_latest_e3sm_unified_chrysalis.sh

export MPAS_SEAICE_DOMAINS_DIR="/lcrc/group/e3sm/public_html/mpas_standalonedata/mpas-seaice/domains"
export MPAS_SEAICE_EXECUTABLE="/home/ac.jeffery/E3SMv2/code/20220926/components/mpas-seaice/seaice_model"

# Run My Program
srun -n 1 python run_testcase.py
