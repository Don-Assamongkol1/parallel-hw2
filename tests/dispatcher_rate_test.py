import subprocess
import os
import filecmp
import glob

import constants


def test_dispatcher_rate():
    print("\n\n\n\n\n\nrunning Dispatcher Rate...")

    W = 1
    n_options = [2, 3, 5, 9, 14, 28]
    parallel_times = []

    for n in n_options:

        T = int((2**20) / (n - 1))

        trial_num = 0
        # run serial code too to verify correctness
        subprocess.run(
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

        mean_parallel_time = 0
        for _ in range(constants.UNIFORM_RERUN_COUNT):
            rv_parallel = subprocess.run(
                [
                    constants.PARALLEL_EXECUTABLE,
                    str(n),
                    str(T),
                    str(W),
                    str(trial_num),
                    constants.UNIFORM,
                ],
                capture_output=True,
                text=True,
            )
            parallel_time = float(rv_parallel.stdout.split(":")[-1].strip())
            mean_parallel_time += parallel_time

            trial_num += 1

        mean_parallel_time /= constants.UNIFORM_RERUN_COUNT
        parallel_times.append(mean_parallel_time)

    print("parallel_times: ", parallel_times)
    ratio = [(2**20) / parallel_times[i] for i in range(len(parallel_times))]
    print("ratio: ", ratio)

    print("testing correctness...")
    serial_filenames = list(sorted(glob.glob("results/serial_output*")))
    for serial_filename in serial_filenames:
        end_of_string = serial_filename.split("serial_output_")[1]
        matching_parallel_file = f"results/parallel_output_{end_of_string}"

        print(serial_filename)
        print(matching_parallel_file)
        if not filecmp.cmp(serial_filename, matching_parallel_file, shallow=False):
            print("Error!")

    print("results seem good!")

    os.system("rm results/*")


"""
In the end we have a bunch of 
parallel_output_<params>_trial_X
...
parallel_output_<params>_trial_Y

serial_output_<params>_
serial_output_<params>_
serial_output_<params>_

We want to match the serial runs against the parallel runs which were run many 
times. 

"""
