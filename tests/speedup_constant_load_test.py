import subprocess
import os
import filecmp
import glob

SERIAL_EXECUTABLE = "./serial"
PARALLEL_EXECUTABLE = "./parallel"
parallel_EXECUTABLE = "./parallel"

# number of times to repeat each experiment so we get representative data
CONSTANT_RERUN_COUNT = 1
UNIFORM_RERUN_COUNT = 5
EXPONENTIAL_RERUN_COUNT = 12

CONSTANT = "C"
UNIFORM = "U"
EXPONENTIAL = "E"


def test_constant_load():
    print("\n\n\n\n\n\nrunning Speedup with Constant Load...")
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

            for _ in range(CONSTANT_RERUN_COUNT):
                rv_serial = subprocess.run(
                    [
                        SERIAL_EXECUTABLE,
                        str(n),
                        str(T),
                        str(W),
                        str(trial_num),
                        CONSTANT,
                    ],
                    capture_output=True,
                    text=True,
                )
                serial_time = float(rv_serial.stdout.split(":")[-1].strip())
                mean_serial_time += serial_time

                rv_parallel = subprocess.run(
                    [
                        PARALLEL_EXECUTABLE,
                        str(n),
                        str(T),
                        str(W),
                        str(trial_num),
                        CONSTANT,
                    ],
                    capture_output=True,
                    text=True,
                )
                parallel_time = float(rv_parallel.stdout.split(":")[-1].strip())
                mean_parallel_time += parallel_time

                trial_num += 1

            mean_serial_time /= CONSTANT_RERUN_COUNT
            mean_parallel_time /= CONSTANT_RERUN_COUNT
            serial_times.append(mean_serial_time)
            parallel_times.append(mean_parallel_time)

        print(f"for W={W}:")

        ratio = [parallel_times[i] / serial_times[i] for i in range(len(serial_times))]
        print("ratio: ", ratio)

    print("testing correctness...")

    # correcntess test here is similar to parallel_overhead_test
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
