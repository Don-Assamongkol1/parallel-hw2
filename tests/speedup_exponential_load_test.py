import subprocess
import os
import filecmp
import glob

import constants


def test_exponential_load():
    print("\n\n\n\n\n\nrunning Speedup with Exponential Load...")
    W_options = [1000, 2000, 4000, 8000]
    n_options = [2, 3, 5, 9, 14, 28]

    for W in W_options:
        serial_times = []
        parallel_times = []

        for n in n_options:
            T = 2**15

            trial_num = 0

            # we will compute an average of the running time for dif seed vals
            mean_serial_time = 0
            mean_parallel_time = 0

            for _ in range(constants.EXPONENTIAL_RERUN_COUNT):
                rv_serial = subprocess.run(
                    [
                        constants.SERIAL_EXECUTABLE,
                        str(n),
                        str(T),
                        str(W),
                        str(trial_num),
                        constants.EXPONENTIAL,
                    ],
                    capture_output=True,
                    text=True,
                )
                serial_time = float(rv_serial.stdout.split(":")[-1].strip())
                mean_serial_time += serial_time

                rv_parallel = subprocess.run(
                    [
                        constants.PARALLEL_EXECUTABLE,
                        str(n),
                        str(T),
                        str(W),
                        str(trial_num),
                        constants.EXPONENTIAL,
                    ],
                    capture_output=True,
                    text=True,
                )
                parallel_time = float(rv_parallel.stdout.split(":")[-1].strip())
                mean_parallel_time += parallel_time

                trial_num += 1

            mean_serial_time /= constants.EXPONENTIAL_RERUN_COUNT
            mean_parallel_time /= constants.EXPONENTIAL_RERUN_COUNT
            serial_times.append(mean_serial_time)
            parallel_times.append(mean_parallel_time)
            # we append at the end of the for n loop, so each speedup corresponds
            # to a fixed W, with increasing n

        print(f"for W={W}:")

        ratio = [parallel_times[i] / serial_times[i] for i in range(len(serial_times))]
        print("parallel_times: ", parallel_times)
        print("serial_times: ", serial_times)
        print("ratio: ", ratio)

    # correcntess test here is similar to parallel_overhead_test
    print("testing correctness...")
    filenames = list(sorted(glob.glob("results/*")))
    for file_idx_one in range(len(filenames) // 2):
        file_idx_two = file_idx_one + len(filenames) // 2
        # print(filenames[file_idx_one])
        # print(filenames[file_idx_two])
        # print("")

        if not filecmp.cmp(
            filenames[file_idx_one], filenames[file_idx_two], shallow=False
        ):
            print("Error!")
    print("results seem good!")

    os.system("rm results/*")
