#include "parallel_module.h"

typedef struct _thread_args_t {
    int thread_idx;  // idx of the queue it should consume from + idx of where it adds checksum to
    long* checksums_array;
    queue_t** queues;
    int T;
    bool dequeueIsSlow;
} thread_args_t;

void* thr_func(void* input) {
    /* typecast arguments */
    thread_args_t* thr_args = (thread_args_t*)input;
    int thread_idx = thr_args->thread_idx;
    queue_t* thread_queue = thr_args->queues[thread_idx];
    bool dequeueIsSlow = thr_args->dequeueIsSlow;

    /* Have worker process its queue while packets remain on them */
    int numPacketsProcessed = 0;
    while (numPacketsProcessed < thr_args->T) {
        volatile Packet_t* packet = malloc(sizeof(volatile Packet_t));

        while (true) {
            if (dequeue(thread_queue, packet, dequeueIsSlow) == SUCCESS) {
                break;
            }
        };

        if (packet->seed != numPacketsProcessed) {
            printf("error! packets seem to be out of order\n");
            return (void *) 1;
        } 
        numPacketsProcessed += 1;
    }


    pthread_exit(NULL);
}

int run_parallel_slow(PacketSource_t* packetSource, long* checksums_array, cmd_line_args_t* args, bool dequeueIsSlow) {
    /* Create numSources many queues */
    queue_t* queues[args->numSources];
    queues[0] = create_queue();

    /* spawn n - 1 worker threads */
    int numThreads = 1;  
    thread_args_t thr_args[numThreads];  // must memory allocate the arg to each thread
    pthread_t thread_ids[numThreads];    // so we can keep track of our threads

    for (int i = 0; i < numThreads; i++) {
        thr_args[i].thread_idx = i;
        thr_args[i].queues = queues;
        thr_args[i].T = args->T;
        thr_args[i].dequeueIsSlow= dequeueIsSlow;

        if (pthread_create(&(thread_ids[i]), NULL, &thr_func, (void*)&thr_args[i]) != 0) {
            printf("error creating thread!\n");
            return 1;
        }
    }

    // Have dispatcher go through and put packets onto the queue
    for (int packetIndex = 0; packetIndex < args->T; packetIndex++) {
        for (int sourceNum = 0; sourceNum < args->numSources; sourceNum++) {
            volatile Packet_t* packet = NULL;

            if (args->distribution == 'C') {
                packet = getConstantPacket(packetSource, sourceNum);
            } else if (args->distribution == 'U') {
                packet = getUniformPacket(packetSource, sourceNum);
            } else if (args->distribution == 'E') {
                packet = getExponentialPacket(packetSource, sourceNum);
            }

            while (true) {
                if (enqueue(queues[sourceNum], packet, !dequeueIsSlow) == SUCCESS) {
                    break;
                }
            };
        }
    }

    /* Join our threads */
    for (int i = 0; i < numThreads; i++) {
        if (pthread_join(thread_ids[i], NULL) != 0) {
            printf("error joining thread!\n");
            return 1;
        }
    }

    /* Free memory */
    for (int i = 0; i < args->numSources; i++) {
        free(queues[i]);
    }

    return EXIT_SUCCESS;
}