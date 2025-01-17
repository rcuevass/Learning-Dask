import utilities
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from timeit import default_timer as timer

from dask.distributed import Client, LocalCluster


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s,%(msecs)3d %(levelname)-8s [%(filename)s:%(lineno)d] - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

fh = TimedRotatingFileHandler('../logs/' + os.path.basename(__file__) + '.log', when='midnight', interval=1)
fh.suffix = '%Y%m%d'
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

log.addHandler(fh)
log.addHandler(ch)

#cluster = LocalCluster(processes=False) # to use threads instead
#client = Client(cluster)


log.info('Executing code ...')


if __name__ == '__main__':
    #
    # Per Dask documentation
    # To set up a local cluster on your machine by instantiating a Dask Client with no arguments
    # This sets up a scheduler in your local process and several processes running single-threaded Workers
    # One can navigate to http://localhost:8787/status to see the diagnostic dashboard if you have Bokeh installed.
    client = Client()
    log.info('Dask client is working now, visit=%s', 'http://localhost:8787/status')

    # set path to reduced csv, only for 2005
    path_to_reduced_csv = '../data/input/Checkouts_By_Title_Data_Lens_2005.csv'
    #
    # timing data read with pandas
    t1 = timer()
    df_pandas = utilities.read_reduced_csv_with_pandas_and_create_month(path_to_reduced_csv, log)
    t2 = timer()
    log.info('Total time processing with pandas, seconds=%d', t2 - t1)

    # timing data read with dask
    t3 = timer()
    df_dask = utilities.read_reduced_csv_with_dask_and_create_month(path_to_reduced_csv, log)
    t4 = timer()
    log.info('Total time processing with Dask, seconds=%d', t4 - t3)

    #
    # set path to whole csv
    path_to_whole_csv = '../data/input/Checkouts_By_Title.csv'
    #
    # timing data read with pandas
    t1 = timer()
    df_pandas = utilities.read_csv_with_pandas_and_count_checkouts(path_to_whole_csv, log)
    t2 = timer()
    log.info('Total time processing with pandas, seconds=%d', t2 - t1)

    # timing data read with dask
    t3 = timer()
    df_dask = utilities.read_csv_with_dask_and_count_checkouts(path_to_whole_csv, log)
    t4 = timer()
    log.info('Total time processing with Dask, seconds=%d', t4 - t3)





