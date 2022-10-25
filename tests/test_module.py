#!/bin/python3

import os

from parallel_overhead_test import test_parallel_overhead


SERIAL_EXECUTABLE = "./serial"
PARALLEL_EXECUTABLE = "./parallel"
SERIAL_QUEUE_EXECUTABLE = "./serial_queue"

CONSTANT = "C"
UNIFORM = "U"
EXPONENTIAL = "E"

print("compiling the code...")
os.system("make serial parallel serial_queue")

test_parallel_overhead()


print("\n\n\n\n\n\nrunning Speedup with Constant Load...")
print("\n\n\n\n\n\nrunning Uniform Load...")
print("\n\n\n\n\n\nrunning Exponentially Distributed Load...")
