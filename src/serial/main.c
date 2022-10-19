#include <stdio.h>
#include <stdlib.h>

#include "packetsource.h"
#include "stopwatch.h"

int main(int argc, char* argv[]) {
    printf("starting serial main\n");

    if (argc != 5) {
        printf("Error! Expected 4 arguments: n, T, D, W");
    }

    int n = atoi(argv[0]);  // number of threads; there are n - 1 workers
    int T = atoi(argv[1]);  // number of packets from each source—(numPackets in the code)
    int D = atoi(argv[2]);  // number of entries in each Lamport queue—(queueDepth in the code).
    int W = atoi(argv[3]);  // expected amount of work per packet—(mean in the code).

    // create our packet sources
    long mean = 7;
    int numSources = n - 1;
    short seed = 1;
    PacketSource_t* packetSources[numSources];

    for (int i = 0; i < numSources; i++) {
        packetSources[i] = createPacketSource(mean, numSources, seed);
    }

    // single-threaded: have our thread grab T packets from each source and compute their checksum

    // clean up
    for (int i = 0; i < numSources; i++) {
        deletePacketSource(packetSources[i]);
    }

    return 0;
}