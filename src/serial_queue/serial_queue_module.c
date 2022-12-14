#include "serial_queue_module.h"

void run_serial_queue(PacketSource_t* packetSource, long* checksums_array, cmd_line_args_t* args) {
    StopWatch_t* stopwatch = malloc(sizeof(StopWatch_t));
    startTimer(stopwatch);

    /* Create numSources many queues */
    queue_t* queues[args->numSources];
    for (int i = 0; i < args->numSources; i++) {
        queues[i] = create_queue();
    }

    int totalPacketsEnqueued = 0;
    int totalPacketsProcessed = 0;

    while (totalPacketsProcessed < args->numSources * args->T) {
        /* Enqueue (n - 1) * D packets, or break earlier if we've enqueued enough total */
        for (int packet_idx = 0; packet_idx < DEPTH; packet_idx++) {
            for (int sourceNum = 0; sourceNum < args->numSources; sourceNum++) {
                volatile Packet_t* packet = NULL;

                if (args->distribution == 'C') {
                    packet = getConstantPacket(packetSource, sourceNum);
                } else if (args->distribution == 'U') {
                    packet = getUniformPacket(packetSource, sourceNum);
                } else if (args->distribution == 'E') {
                    packet = getExponentialPacket(packetSource, sourceNum);
                }

                if (enqueue(queues[sourceNum], packet, false) == FAILURE) {
                    printf("You should never see this line; we predictably know how much is enqueued\n");
                }

                totalPacketsEnqueued += 1;
            }

            if (totalPacketsEnqueued >= args->numSources * args->T) {
                break;
            }
        }

        /* Process the packets */
        for (int packet_idx = 0; packet_idx < DEPTH; packet_idx++) {
            for (int sourceNum = 0; sourceNum < args->numSources; sourceNum++) {
                volatile Packet_t* packet = malloc(sizeof(volatile Packet_t));
                if (dequeue(queues[sourceNum], packet, false) == FAILURE) {
                    printf("You should never see this line; we predictably know how much is dequeued\n");
                }

                checksums_array[sourceNum] += getFingerprint(packet->iterations, packet->seed);

                totalPacketsProcessed += 1;
            }

            if (totalPacketsProcessed >= args->numSources * args->T) {
                break;
            }
        }
    }

    /* Free memory */
    for (int i = 0; i < args->numSources; i++) {
        free(queues[i]);
    }

    stopTimer(stopwatch);
    double elapsed_time = getElapsedTime(stopwatch);
    printf("elapsed_time: %f\n", elapsed_time);
    free(stopwatch);
}
