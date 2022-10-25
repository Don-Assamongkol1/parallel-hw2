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


def test_parallel_overhead():
    print("\n\n\n\n\n\nrunning Parallel Overhead...")
    W_options = [200, 400, 800]
    n_options = [2, 9, 14]

    trial_num = 0
    for n in n_options:
        serial_times = []
        serial_queue_times = []

        for W in W_options:
            T = int((2**20) / n / W)
            rv_serial = subprocess.run(
                [SERIAL_EXECUTABLE, str(n), str(T), str(W), str(trial_num), UNIFORM],
                capture_output=True,
                text=True,
            )
            serial_times.append(float(rv_serial.stdout.split(":")[-1].strip()))

            rv_serial_queue = subprocess.run(
                [
                    SERIAL_QUEUE_EXECUTABLE,
                    str(n),
                    str(T),
                    str(W),
                    str(trial_num),
                    UNIFORM,
                ],
                capture_output=True,
                text=True,
            )
            serial_queue_times.append(
                float(rv_serial_queue.stdout.split(":")[-1].strip())
            )

            trial_num += 1

        print(f"for n={n}:")
        print("serial_queue_times: ", serial_queue_times)
        print("serial_times: ", serial_times)

        ratio = [
            serial_queue_times[i] / serial_times[i] for i in range(len(serial_times))
        ]
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
