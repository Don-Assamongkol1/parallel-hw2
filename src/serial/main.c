#include <stdio.h>
#include <stdlib.h>

#include "fingerprint.h"
#include "packetsource.h"
#include "stopwatch.h"

int main(int argc, char* argv[]) {
    printf("starting serial main...\n");

    if (argc != 5) {
        printf("Error! Expected 4 arguments: n, T, W trial_num\n");
        return 0;
    }
    // argv[0] is the name of the program eg "./serial"
    int n = atoi(argv[1]);          // number of threads; there are n - 1 workers
    int T = atoi(argv[2]);          // number of packets from each source—(numPackets in the code)
    int W = atoi(argv[3]);          // expected amount of work per packet—(mean in the code).
    int trial_num = atoi(argv[4]);  // expected amount of work per packet—(mean in the code).

    // create our packet source
    long mean = (long)W;
    int numSources = n - 1;
    short seed = (short)trial_num;

    PacketSource_t* packetSource = createPacketSource(mean, numSources, seed);

    // create our checksums array, where we store the checksum for each source
    long checksums_array[numSources];
    for (int i = 0; i < numSources; i++) {
        checksums_array[i] = 0;
    }

    // single-threaded: have our thread grab T packets from each source and compute their checksum
    for (int packetNum = 0; packetNum < T; packetNum++) {
        for (int sourceNum = 0; sourceNum < numSources; sourceNum++) {
            volatile Packet_t* packet = getUniformPacket(packetSource, sourceNum);
            checksums_array[sourceNum] += getFingerprint(packet->iterations, packet->seed);
        }
    }

    // write output module
    create_output(checksums_array, numSources, n, T, W, trial_num);

    // clean up
    deletePacketSource(packetSource);

    return 0;
}