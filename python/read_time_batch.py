"""
Script Name: read_cpu_time_batch.py
Author: Tom, cstandy
Description: Playground for reading the cpu time.
"""

from read_cpu_time import stat_proc_time
from read_elapsed_time import elapsed_time
import numpy as np

################################################################################
# Main func
################################################################################

if __name__ == '__main__':

    config = 'u13_cr0p333_16QAM'

    # Read and print the CPU time
    for mu in range(0, 4):
        for num_worker in [0, 1, 2, 4, 8, 16]:
            filename = '../log/four-config_mu_worker/{}_mu{}_w{}.log'.format(
                config, mu, num_worker)
            avg_cpu_time = stat_proc_time(filename=filename, stat='avg')[0]
            print('{}, mu = {}, num_worder = {}: avg cpu time = {:.2f}'.format(
                config, mu, num_worker, avg_cpu_time))
            
    print('-----------------------------------------------')

    # Read and print the elapsed time
    for mu in range(0, 4):
        for num_worker in [0, 1, 2, 4, 8, 16]:
            filename = '../log/four-config_mu_worker/{}_mu{}_w{}.log'.format(
                config, mu, num_worker)
            time = elapsed_time(filename=filename)[0]
            avg_elapsed_time = np.mean(np.array(time))
            print('{}, mu = {}, num_worder = {}: avg elapsed time = {:.2f}'
                  .format(config, mu, num_worker, avg_elapsed_time))
