#ifndef TYPES_H
#define TYPES_H

typedef struct {
    int n;
    int T;
    int W;
    int trial_num;
    int numSources;
} cmd_line_args_t;

/* Return codes for queue operations */
#define SUCCESS 0
#define FAILURE 1

/* program codes to name output files */
#define SERIAL 110
#define PARALLEL 111
#define SERIAL_QUEUE 112

/* Writing to output */
#define MAX_LINE_LENGTH 100000
#define MAX_STRING_LENGTH 100

#endif