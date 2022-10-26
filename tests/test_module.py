#!/bin/python3

import os

from parallel_overhead_test import test_parallel_overhead
from dispatcher_rate_test import test_dispatcher_rate


SERIAL_EXECUTABLE = "./serial"
PARALLEL_EXECUTABLE = "./parallel"
SERIAL_QUEUE_EXECUTABLE = "./serial_queue"

CONSTANT = "C"
UNIFORM = "U"
EXPONENTIAL = "E"

print("compiling the code...")
os.system("make serial parallel serial_queue")

# test_parallel_overhead()
test_dispatcher_rate()


print("\n\n\n\n\n\nrunning Speedup with Constant Load...")
print("\n\n\n\n\n\nrunning Uniform Load...")
print("\n\n\n\n\n\nrunning Exponentially Distributed Load...")
