#include "packetsource.h"

typedef struct _queue {
    volatile int head;
    volatile int tail;
    Packet_t** packet_array;
} queue_t;

queue_t* create_queue();  // returns a malloc'd queue

int dequeue(queue_t* queue, Packet_t* item);  // item is a write-out parameter

int enqueue(queue_t* queue, Packet_t* item);
