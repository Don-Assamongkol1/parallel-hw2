CFLAGS = -O3 -Wall -I src/include -pthread 
SRCS_SERIAL = src/utils/* src/serial/* src/output/*
SRCS_PARALLEL = src/utils/* src/parallel/* src/output/* src/queue/*

serial: $(SRCS) ./src/include ./src/serial
	gcc $(CFLAGS) -o serial $(SRCS_SERIAL)

parallel: $(SRCS) ./src/include ./src/parallel
	gcc $(CFLAGS) -o parallel $(SRCS_PARALLEL)

clean:
	rm serial