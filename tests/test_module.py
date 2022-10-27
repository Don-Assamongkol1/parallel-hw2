#!/bin/python3

import os

from parallel_overhead_test import test_parallel_overhead
from dispatcher_rate_test import test_dispatcher_rate
from speedup_uniform_load_test import test_uniform_load
from speedup_exponential_load_test import test_exponential_load
from speedup_constant_load_test import test_constant_load


SERIAL_EXECUTABLE = "./serial"
PARALLEL_EXECUTABLE = "./parallel"
SERIAL_QUEUE_EXECUTABLE = "./serial_queue"

CONSTANT = "C"
UNIFORM = "U"
EXPONENTIAL = "E"

print("compiling the code...")
os.system("make serial parallel serial_queue")

# test_parallel_overhead()
# test_dispatcher_rate()
test_uniform_load()
# test_exponential_load()
# test_constant_load()
