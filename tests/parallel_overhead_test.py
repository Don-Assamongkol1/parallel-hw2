import subprocess
import os
import filecmp
import glob

import constants


def test_parallel_overhead():
    print("\n\n\n\n\n\nrunning Parallel Overhead...")

    W_options = [200, 400, 800] 
    n_options = [2, 9, 14]

    for n in n_options:
        serial_times = []
        serial_queue_times = []

        for W in W_options:
            T = int((2**20) / n / W)

            # we will compute an average of the running time for dif seed vals
            mean_serial_time = 0
            mean_serial_queue_time = 0

            trial_num = 0
            for _ in range(constants.UNIFORM_RERUN_COUNT):
                rv_serial = subprocess.run(
                    [
                        constants.SERIAL_EXECUTABLE,
                        str(n),
                        str(T),
                        str(W),
                        str(trial_num),
                        constants.UNIFORM,
                    ],
                    capture_output=True,
                    text=True,
                )
                serial_time = float(rv_serial.stdout.split(":")[-1].strip())
                mean_serial_time += serial_time

                rv_serial_queue = subprocess.run(
                    [
                        constants.SERIAL_QUEUE_EXECUTABLE,
                        str(n),
                        str(T),
                        str(W),
                        str(trial_num),
                        constants.UNIFORM,
                    ],
                    capture_output=True,
                    text=True,
                )
                serial_queue_time = float(rv_serial_queue.stdout.split(":")[-1].strip())
                mean_serial_queue_time += serial_queue_time

                trial_num += 1

            mean_serial_time /= constants.UNIFORM_RERUN_COUNT
            mean_serial_queue_time /= constants.UNIFORM_RERUN_COUNT
            serial_times.append(mean_serial_time)
            serial_queue_times.append(mean_serial_queue_time)

        print(f"for n={n}:")

        ratio = [
            serial_queue_times[i] / serial_times[i] for i in range(len(serial_times))
        ]
        print("serial_queue_times: ", serial_queue_times)
        print("serial_times: ", serial_times)
        print("ratio: ", ratio)

    print("testing correctness...")

    # for explanation of correctness code see below
    filenames = list(sorted(glob.glob("results/*")))
    for file_idx_one in range(len(filenames) // 2):
        file_idx_two = file_idx_one + len(filenames) // 2
        if not filecmp.cmp(
            filenames[file_idx_one], filenames[file_idx_two], shallow=False
        ):
            print("Error!")
    print("results seem good!")

    os.system("rm results/*")

"""
Correctness testing explanation
We have a bunch of files like [
    parallel_output_n_2_T_655_W_800_trial_0_uniform.txt
    ... 
    // the name of the last parallel output 
    serial_output_n_2_T_655_W_800_trial_0_uniform
    ...
    // the name of the last serial output
]

So we just want to compare the files from each group, parallel or serial, 
sequentially.
"""