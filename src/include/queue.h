#include "types.h"

queue_t* create_queue();  // returns a malloc'd queue

int dequeue(queue_t* queue, Packet_t* packet);  // packet is a write-out parameter

int enqueue(queue_t* queue, Packet_t* packet);
