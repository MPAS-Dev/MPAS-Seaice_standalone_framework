import os
from plot_testcase import plot_testcase
from plot_testcase_forcing import plot_testcase_forcing

#-------------------------------------------------------------------------------

def run_testcase():

    MPAS_SEAICE_EXECUTABLE = os.environ.get('MPAS_SEAICE_EXECUTABLE')
    MPAS_SEAICE_TESTCASES_RUN_COMMAND = os.environ.get('MPAS_SEAICE_TESTCASES_RUN_COMMAND')
    if (MPAS_SEAICE_TESTCASES_RUN_COMMAND is None):
        MPAS_SEAICE_TESTCASES_RUN_COMMAND = ""
    MPAS_SEAICE_DOMAINS_DIR = os.environ.get('MPAS_SEAICE_DOMAINS_DIR')

    # copy namelist and streams file
    os.system("cp ../../configurations/ispol_bgc_single_cell/namelist.seaice .")
    os.system("cp ../../configurations/ispol_bgc_single_cell/streams.seaice .")

    # forcing
    os.system("python %s/domain_sc_-67.9_-54.4/get_domain.py" %(MPAS_SEAICE_DOMAINS_DIR))

    # run MPAS-Seaice
    os.system("%s %s" %(MPAS_SEAICE_TESTCASES_RUN_COMMAND, MPAS_SEAICE_EXECUTABLE))

    # plot output
    plot_testcase()

    # plot forcing
    plot_testcase_forcing()

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    run_testcase()
