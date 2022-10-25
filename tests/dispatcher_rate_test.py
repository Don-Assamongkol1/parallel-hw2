import subprocess
import os
import filecmp
import glob

SERIAL_EXECUTABLE = "./serial"
PARALLEL_EXECUTABLE = "./parallel"
SERIAL_QUEUE_EXECUTABLE = "./serial_queue"

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
        parallel_times.append(float(rv_parallel.stdout.split(":")[-1].strip()))

        trial_num += 1

        ratio = [(2**20) / serial_times[i] for i in range(len(serial_times))]
        print("ratio: ", ratio)

    print("testing correctness...")
    filenames = list(sorted(glob.glob("results/*")))
    for file_idx_one in range(len(filenames) // 2):
        file_idx_two = file_idx_one + len(filenames) // 2
        if not filecmp.cmp(
            filenames[file_idx_one], filenames[file_idx_two], shallow=False
        ):
            print("Error!")
    print("results seem good!")

    os.system("rm results/*")
