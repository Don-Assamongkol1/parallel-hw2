CFLAGS = -O3 -Wall -I src/include -pthread 
SRCS = src/utils/* src/serial/* src/output/*

serial: $(SRCS) ./src/include
	gcc $(CFLAGS) -o serial $(SRCS)

clean:
	rm serial