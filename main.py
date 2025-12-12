from time import time

from source.utilities.logger_setup import setup_logger
from source.utilities.time_descriptor import time_descriptor
from source.utils_run import main


logger = setup_logger()

if __name__ == "__main__":
    start_time = time()
    main()
    estimated_time = int(time() - start_time)
    time_descriptor(estimated_time)
