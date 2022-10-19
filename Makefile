CFLAGS = -O3 -Wall -I src/include -pthread 
SRCS = src/utils/* src/serial/*

serial: $(SRCS) ./src/include
	gcc $(CFLAGS) -o serial $(SRCS)

clean:
	rm serial