#include "serial_module.h"

void run_serial(PacketSource_t* packetSource, long* checksums_array, cmd_line_args_t* args) {
    for (int packetNum = 0; packetNum < args->T; packetNum++) {
        for (int sourceNum = 0; sourceNum < args->numSources; sourceNum++) {
            volatile Packet_t* packet = getUniformPacket(packetSource, sourceNum);
            checksums_array[sourceNum] += getFingerprint(packet->iterations, packet->seed);
        }
    }
}
