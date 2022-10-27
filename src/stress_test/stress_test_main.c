#include <stdio.h>
#include <stdlib.h>

#include "output_module.h"
#include "packetsource.h"
#include "parallel_module_slow.h"
#include "stopwatch.h"
#include "types.h"

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Error! Expected to be called like ./stress_test <D or E> \n");
        return 0;
    }
    // 'D' arg means dequeue is slow, 'E' arg means enqueue is slow 

    cmd_line_args_t* args = malloc(sizeof(cmd_line_args_t));  // commonly used variables
    args->n = 2;                                  // number of threads; there are n - 1 workers ; recall argv[0] is ./<executable_name>
    args->T = 100000;                                  // number of packets from each source—(numPackets in the code)
    args->W = 1;
    args->trial_num = 0;                          // expected amount of work per packet—(mean in the code).
    args->distribution = 'C';                          // distribution type either 'C', 'U', 'E'
    args->numSources = args->n - 1;


    // create our packet source
    PacketSource_t* packetSource = createPacketSource((long)args->W, args->numSources, (short)args->trial_num);

    // create our checksums array, where we store the checksum for each source
    long checksums_array[args->numSources];
    for (int i = 0; i < args->numSources; i++) {
        checksums_array[i] = 0;
    }

    bool dequeueIsSlow = true;
    if (argv[1][0] == 'D') {
        dequeueIsSlow = true;
    }
    if (argv[1][0] == 'E') {
        dequeueIsSlow = false;
    }

    // single-threaded: have our thread grab T packets from each source and compute their checksum
    run_parallel_slow(packetSource, checksums_array, args, dequeueIsSlow);

    // clean up
    deletePacketSource(packetSource);

    return 0;
}