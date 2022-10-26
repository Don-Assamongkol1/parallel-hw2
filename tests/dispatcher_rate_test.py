import subprocess
import os
import filecmp
import glob

SERIAL_EXECUTABLE = "./serial"
PARALLEL_EXECUTABLE = "./parallel"
SERIAL_QUEUE_EXECUTABLE = "./serial_queue"

# number of times to repeat each experiment so we get representative data
UNIFORM_RERUN_COUNT = 5
EXPONENTIAL_RERUN_COUNT = 12

CONSTANT = "C"
UNIFORM = "U"
EXPONENTIAL = "E"


def test_dispatcher_rate():
    print("\n\n\n\n\n\nrunning Dispatcher Rate...")

    W = 1
    n_options = [2, 3, 5, 9, 14, 28]
    parallel_times = []

    trial_num = 0
    for n in n_options:

        T = int((2**20) / (n - 1))
        mean_parallel_time = 0

        for _ in range(UNIFORM_RERUN_COUNT):
            rv_parallel = subprocess.run(
                [
                    PARALLEL_EXECUTABLE,
                    str(n),
                    str(T),
                    str(W),
                    str(trial_num),
                    UNIFORM,
                ],
                capture_output=True,
                text=True,
            )
            parallel_time = float(rv_parallel.stdout.split(":")[-1].strip())
            mean_parallel_time += parallel_time

            trial_num += 1

        mean_parallel_time /= UNIFORM_RERUN_COUNT
        parallel_times.append(mean_parallel_time)

    ratio = [(2**20) / parallel_times[i] for i in range(len(parallel_times))]
    print("ratio: ", ratio)

    os.system("rm results/*")
