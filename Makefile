CFLAGS = -O3 -Wall -Werror -I src/include -pthread 
SRCS_SERIAL = src/utils/* src/serial/* src/output/*
SRCS_PARALLEL = src/utils/* src/parallel/* src/output/* src/queue/*
SRCS_SERIAL_QUEUE = src/utils/* src/serial_queue/* src/output/* src/queue/*

serial: $(SRCS) ./src/include/* ./src/serial/*
	gcc $(CFLAGS) -o serial $(SRCS_SERIAL)

parallel: $(SRCS) ./src/include/* ./src/parallel/* ./src/queue/*
	gcc $(CFLAGS) -o parallel $(SRCS_PARALLEL)

serial_queue: $(SRCS) ./src/include/* ./src/serial_queue/* ./src/queue/*
	gcc $(CFLAGS) -o serial_queue $(SRCS_SERIAL_QUEUE)

all:
	make serial parallel serial_queue

clean:
	rm serial parallel serial_queue