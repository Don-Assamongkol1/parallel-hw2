#include "queue.h"
#define DEPTH 32  // a fixed amount for this assignment

queue_t* create_queue() {
    queue_t* queue = malloc(sizeof(queue_t));
    queue->head = 0;
    queue->tail = 0;

    // create an array of (packet pointers) of depth D
    queue->packet_array = malloc(sizeof(Packet_t*) * DEPTH);
    queue->depth = DEPTH;
}

int enqueue(queue_t* queue, Packet_t* packet) {
    if ((queue->tail - queue->head) == queue->depth) {
        return FAILURE;
    }
    queue->packet_array[queue->tail % queue->depth] = packet;
    queue->tail += 1;
}

int dequeue(queue_t* queue, Packet_t* packet) {
    if ((queue->tail - queue->head) == 0) {
        return FAILURE;
    }
    packet = queue->packet_array[queue->head % queue->depth];
    queue->head += 1;
    return SUCCESS;
}
