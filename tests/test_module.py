#!/bin/python3

from ast import Param
import subprocess
import os
import filecmp


print("running parallel overhead experiment")

W_options = [200, 400, 800]
n_options = [2, 9, 14]

SERIAL_EXECUTABLE = "./serial"
PARALLEL_EXECUTABLE = "./parallel"
SERIAL_QUEUE_EXECUTABLE = "./serial_queue"

CONSTANT = "C"
UNIFORM = "U"
EXPONENTIAL = "E"

# args are
# n (int), T (int), W (int), trial_num (int), distribution ('C', 'U', 'E')

trial_num = 0
for W in W_options:
    for n in n_options:
        T = int(2**20 / n / W)
        rv = subprocess.run(
            [SERIAL_EXECUTABLE, str(n), str(T), str(W), str(trial_num), UNIFORM],
            capture_output=True,
            text=True,
        )
        rv = subprocess.run(
            [PARALLEL_EXECUTABLE, str(n), str(T), str(W), str(trial_num), UNIFORM],
            capture_output=True,
            text=True,
        )
        trial_num += 1
